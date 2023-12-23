import json
from pathlib import Path
from pydantic import BaseModel
from typing import List, Any
from nonebot import require
from nonebot.adapters import Event

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import (
    on_alconna,
    Alconna,
    Option,
    AlconnaMatches,
    Args,
    Arparma,
    Subcommand,
)
from nonebot_plugin_userinfo import get_user_info

from utils import JsonDataStorage, not_llbds_message_event, get_media_bot, get_bds_bot


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


alc = Alconna(
    "/whitelist",
    Subcommand(
        "add",
        Args["player_id", str],
    ),
    Subcommand(
        "remove",
        Args["player_id", str],
    ),
    Option("list"),
)


whitelist = on_alconna(alc, rule=not_llbds_message_event, block=False, priority=5)


@whitelist.handle()
async def _(
    event: Event,
    result: Arparma = AlconnaMatches(),
):
    if (media_bot := get_media_bot()) is None:
        return None

    if (bds_bot := get_bds_bot()) is None:
        return None

    user_info = await get_user_info(media_bot, event, event.get_user_id())

    if result.find("add"):
        player_id = result.query[str]("add.player_id").strip()

        if player_id == "":
            await whitelist.finish("格式错误，请使用 wl add [XboxID] 添加白名单")

        if player_storage.exist(user_info.user_id):
            await bds_bot.runcmdEx(
                f"whitelist remove {player_storage.get_data(user_info.user_id).player_id}"
            )
            player_storage.change_data(user_info.user_id, "player_id", player_id)
            await bds_bot.runcmdEx(f"whitelist add {player_id}")
            await whitelist.finish(
                f"你已绑定过白名单（已自动添加 {player_id} 到白名单，上一个 XboxID 的白名单已失效）"
            )
        else:
            player_storage.add_user(user_info.user_id, player_id)
            await bds_bot.runcmdEx(f"whitelist add {player_id}")
            await whitelist.finish(f"已添加 {player_id} 到白名单")

    if result.find("remove"):
        data = player_storage.get_data(user_info.user_id)
        player_id = result.query[str]("remove.player_id").strip()
        await bds_bot.runcmdEx(f"whitelist remove {data.player_id}")
        if player_storage.exist(user_info.user_id):
            player_storage.change_data(user_info.user_id, "player_id", "")
        await whitelist.finish(f"已删除 {player_id} 的白名单")

    if result.find("list"):
        whitelist_data = (await bds_bot.runcmdEx("whitelist list"))["output"]
        await whitelist.finish(whitelist_data)
