import json
from pathlib import Path
from pydantic import BaseModel
from typing import List, Any
from nonebot import on_command, require
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.red import MessageEvent, Message

require("init")

from utils import JsonDataStorage
from plugin.forward import bds_server


class Player(BaseModel):
    user_id: str
    player_id: str


class PlayerStorage(JsonDataStorage):
    def __init__(self):
        super().__init__(Player, Path.cwd() / "data" / "player.json")
        if not self.file_path.exists():
            self.file_path.parent.mkdir()
            with open(self.file_path, "w", encoding="UTF-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)
            self.data = []
        else:
            self.data: List[Player] = self.load_as_list()

    def add_user(self, user_id: str, player_id: str) -> Player:
        data = Player(user_id=user_id, player_id=player_id)
        self.data.append(data)
        self.save_as_list(self.data)
        return data

    def change_data(self, user_id: str, key: str, value: Any) -> Player:
        symbol = False
        for idx, data in enumerate(self.data):
            if data.user_id == user_id:
                setattr(self.data[idx], key, value)
                symbol = True
                break

        if not symbol:
            self.add_user(user_id)
            self.change_data(user_id, key, value)

        self.save_as_list(self.data)
        return self.data[idx]

    def get_data(self, user_id: str) -> Player:
        for data in self.data:
            if data.user_id == user_id:
                return data
        return self.add_user(user_id)

    def exist(self, user_id: str) -> bool:
        for data in self.data:
            if data.user_id == user_id:
                return True
        return False


player_storage = PlayerStorage()


@on_command("wl", block=False).handle()
async def _(matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split(maxsplit=1)
    sub_arg = args[0].strip()

    if sub_arg == "add":
        player_id = arg.extract_plain_text().replace(sub_arg, "").strip()

        if player_id == "":
            await matcher.finish("格式错误，请使用 wl add [XboxID] 添加白名单")

        if player_storage.exist(event.senderUin):
            await bds_server.run_cmd(
                f"whitelist remove {player_storage.get_data(event.senderUin).player_id}"
            )
            player_storage.change_data(event.senderUin, "player_id", player_id)
            await bds_server.run_cmd(f"whitelist add {player_id}")
            await matcher.finish(f"你已绑定过白名单（已自动添加 {player_id} 到白名单，上一个 XboxID 的白名单已失效）")
        else:
            player_storage.add_user(event.senderUin, player_id)
            await bds_server.run_cmd(f"whitelist add {player_id}")
            await matcher.finish(f"已添加 {player_id} 到白名单")

    if sub_arg == "remove":
        data = player_storage.get_data(event.senderUin)
        await bds_server.run_cmd(f"whitelist remove {data.player_id}")
        if player_storage.exist(event.senderUin):
            player_storage.change_data(event.senderUin, "player_id", "")
        await matcher.finish(f"已删除 {player_id} 的白名单")
