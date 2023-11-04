import json
import time
import asyncio
from pathlib import Path
from typing import List

from .model import Payload, CommandType, SenderType


class Server(object):
    def __init__(self, bds_dir):
        self._bds_dir = Path(bds_dir)
        self._connect_dir = self._bds_dir / "connect"
        self._echo_offset = 0

        self._connect_dir.mkdir(exist_ok=True)

    async def _receive_for_sending(self, echo: str):
        """获取 BDS 执行指令的返回值"""
        payload_files: List[Path] = [
            item for item in self._connect_dir.iterdir() if item.is_file()
        ]
        for payload_file in payload_files:
            payload: Payload = json.loads(payload_file.read_text())
            if (
                payload["echo"] == echo
                and payload["command_type"] == CommandType.result
                and payload["sender_type"] == SenderType.bds
            ):
                payload_file.unlink()
                return payload["context"]

    async def receive_for_event(self):
        """获得 BDS 推送的游戏事件"""
        payload_files: List[Path] = [
            item for item in self._connect_dir.iterdir() if item.is_file()
        ]
        events = []
        for payload_file in payload_files:
            payload: Payload = json.loads(payload_file.read_text())
            if (
                payload["command_type"] == CommandType.command
                and payload["sender_type"] == SenderType.bds
            ):
                events.append(json.loads(payload["context"]))
                payload_file.unlink()

        return events

    async def run_cmd(self, cmd: str):
        """运行 BDS 命令"""
        echo = str(self._echo_offset)
        self._echo_offset += 1

        payload = Payload(
            sender_type=SenderType.bot,
            command_type=CommandType.command,
            context=cmd,
            echo=echo,
        )
        (self._connect_dir / f"{echo}.txt").write_text(json.dumps(payload), "UTF-8")

        start_time = time.time()

        while True:
            # 5s 超时
            if time.time() - start_time > 5:
                raise TimeoutError("Failed to connect to BDS.")

            if (result := await self._receive_for_sending(echo)) is not None:
                return result

            await asyncio.sleep(0.05)
