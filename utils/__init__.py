import json
from typing import Any, Dict, Union, List, Optional
from pydantic import BaseModel
from pathlib import Path

from nonebot import require, get_bots, get_driver
from nonebot.adapters import Bot, Event
from nonebot.adapters.llbds.bot import Bot as BDSBot
from nonebot.adapters.llbds.event import MessageEvent as BDSMessageEvent

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_alconna.uniseg import (
    At,
    AtAll,
    Card,
    File,
    Text,
    Audio,
    Emoji,
    Image,
    Other,
    Reply,
    Video,
    Voice,
)


def process_message(unimsg: UniMsg) -> str:
    result = ""
    for seg in unimsg:
        if isinstance(seg, At):
            result += f"@{seg.display or seg.target} "
        elif isinstance(seg, AtAll):
            result += "@全体成员 "
        elif isinstance(seg, Card):
            result += "[卡片]"
        elif isinstance(seg, File):
            result += "[文件]"
        elif isinstance(seg, Text):
            result += seg.text
        elif isinstance(seg, Audio):
            result += "[语音]"
        elif isinstance(seg, Emoji):
            result += "[表情]"
        elif isinstance(seg, Image):
            result += "[图片]"
        elif isinstance(seg, Other):
            result += "[其他]"
        elif isinstance(seg, Reply):
            result += f"[回复] {seg.msg or ''}"
        elif isinstance(seg, Video):
            result += "[视频]"
        elif isinstance(seg, Voice):
            result += "[语音]"
        else:
            result += "[未知]"
    return result


class JsonDataStorage:
    """基于 Pydantic 的 JSON 数据读写方法"""

    def __init__(
        self,
        model: Union[BaseModel, List[BaseModel]] = None,
        file_path: Union[str, Path] = "",
    ):
        """基于 Pydantic 的 JSON 数据读写方法

        参数:
        - model (Union[BaseModel, List[BaseModel]], optional): 父类为 BaseModel 的模型
        - file_path (Union[str, Path]): 要保存数据的文件路径
        """
        if not file_path:
            raise ValueError("File path is required.")
        self.model = model
        self.file_path = file_path

    def load(self) -> "JsonDataStorage.model":
        """
        从指定的文件路径加载 JSON 数据并将其转换为模型对象

        返回:
        - BaseModel: 解析后的模型对象
        """
        return self.model.parse_file(self.file_path)

    def load_as_list(self) -> List["JsonDataStorage.model"]:
        """
        从指定的文件路径加载 JSON 数据并将其转换为模型对象列表

        返回:
        - List[BaseModel]: 解析后的模型对象列表
        """
        with open(self.file_path, "r", encoding="UTF-8") as file:
            data: List[Dict[Any, Any]] = json.load(file)
        return [self.model.parse_obj(d) for d in data]

    def save(self, data: BaseModel) -> None:
        """
        将模型对象转换为 JSON 数据并保存到指定的文件路径

        参数:
        - data (BaseModel): 要保存的模型对象
        """
        with open(self.file_path, "w", encoding="UTF-8") as file:
            json.dump(data.dict(), file, indent=4)

    def save_as_list(self, data: List[BaseModel]) -> None:
        """
        将模型对象转换为列表 JSON 数据并保存到指定的文件路径

        参数:
        - data (List[BaseModel]): 要保存的模型对象列表
        """
        if type(data) != list:
            raise ValueError("Only list-like object is suitable for this method.")
        with open(self.file_path, "w", encoding="UTF-8") as file:
            json.dump([d.dict() for d in data], file, indent=4)


def is_llbds_message_event(event: Event) -> bool:
    return isinstance(event, BDSMessageEvent)


def not_llbds_message_event(event: Event) -> bool:
    return not isinstance(event, BDSMessageEvent)


def get_bds_bot() -> Optional[BDSBot]:
    return get_bots().get(getattr(get_driver().config, "llbds_server_id"))


def get_media_bot() -> Optional[Bot]:
    bots = [
        bot
        for bot_id, bot in get_bots().items()
        if bot_id != getattr(get_driver().config, "llbds_server_id")
    ]
    if len(bots) == 0:
        return None
    return bots[0]
