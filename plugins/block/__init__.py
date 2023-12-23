from typing import Union
from nonebot import require
from nonebot.adapters import Bot, Event
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.adapters.llbds.event import Event as BDSEvent

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Target
from nonebot_plugin_alconna.uniseg.params import _target

from config import get_config


config = get_config()


def weak_equal(a: Union[str, int], b: Union[str, int]) -> bool:
    if isinstance(a, int):
        a = str(a)
    if isinstance(b, int):
        b = str(b)
    return a == b


@run_preprocessor
async def check_target(bot: Bot, event: Event):
    if isinstance(event, BDSEvent):
        return None

    target: Target = _target(bot, event)

    if not weak_equal(target.id, config.bds_target_id):
        raise IgnoredException("Check target failed.")
