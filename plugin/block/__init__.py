from nonebot import get_driver
from nonebot.adapters.red import MessageEvent
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException


config = get_driver().config


@run_preprocessor
async def _(event: MessageEvent):
    if int(event.peerUin) != getattr(config, "bds_group"):
        raise IgnoredException("")
