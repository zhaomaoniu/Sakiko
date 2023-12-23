from nonebot import on_command
from nonebot.matcher import Matcher

from utils import not_llbds_message_event, get_bds_bot


@on_command(
    "list", rule=not_llbds_message_event, block=False, priority=15
).handle()
async def _(matcher: Matcher):
    if (bds_bot := get_bds_bot()) is None:
        return None

    cmd_result = (await bds_bot.runcmdEx("list"))["output"]
    try:
        players = cmd_result.split("\n")[1].split(",")
        await matcher.finish(f"当前共有 {len(players)} 人在线：\n" + ",".join(players))
    except IndexError:
        await matcher.finish("当前无人在线")
