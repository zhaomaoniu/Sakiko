from typing import List, Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import get_bot, get_driver, on_message, require
from nonebot.adapters.red import Bot, MessageEvent

from utils import process_message

require("init")

from plugin.init import bds_server, config


@on_message().handle()
async def _(event: MessageEvent):
    await bds_server.run_cmd(
        f"say <{event.sendMemberName or event.sendNickName}> {process_message(event.elements)}"
    )


@get_driver().on_bot_connect
async def _():
    bot: Bot = get_bot()

    async def send(msg: str):
        return await bot.send_group_message(getattr(config, "bds_group"), msg)

    async def notice():
        request_datas: List[Dict] = await bds_server.receive_for_event()
        for request_data in request_datas:
            if request_data.get("type") and request_data.get("data"):
                match request_data["type"]:
                    case "onChat":
                        player = request_data["data"]["player"]
                        msg: str = request_data["data"]["msg"]
                        await send(f"<{player['name']}> {msg}")

                    case "onPlayerDie":
                        player = request_data["data"]["player"]
                        source = request_data["data"]["source"]
                        if source["name"] is not None:
                            await send(f"{player['name']} 因 {source['name']} 似了，好似喵")
                        else:
                            await send(f"{player['name']} 似了，好似喵")

                    case "onJoin":
                        player = request_data["data"]["player"]
                        await send(f"{player['name']} 加入了游戏")

                    case "onLeft":
                        player = request_data["data"]["player"]
                        await send(f"{player['name']} 退出了游戏")

    # 定时发送
    scheduler = AsyncIOScheduler()
    # 每 0.05s 执行一次
    scheduler.add_job(notice, "interval", seconds=0.05)
    scheduler.start()
