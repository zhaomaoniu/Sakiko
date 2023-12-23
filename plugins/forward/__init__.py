import json
from nonebot import require, on_message, on_notice
from nonebot.adapters import Event
from nonebot.adapters.llbds.event import MessageEvent as BDSMessageEvent
from nonebot.adapters.llbds.event import PreJoinEvent, LeftEvent, PlayerDieEvent

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import UniMessage, Target, UniversalMessage
from nonebot_plugin_userinfo import get_user_info

from utils import (
    process_message,
    not_llbds_message_event,
    is_llbds_message_event,
    get_media_bot,
    get_bds_bot,
)
from config import get_config


config = get_config()


forward_to_bds = on_message(rule=not_llbds_message_event, block=False, priority=10)
forward_to_media = on_message(rule=is_llbds_message_event, block=False, priority=10)


@forward_to_bds.handle()
async def _(
    event: Event,
    unimsg: UniMessage = UniversalMessage(),
):
    if (media_bot := get_media_bot()) is None:
        return None

    if (bds_bot := get_bds_bot()) is None:
        return None

    user_info = await get_user_info(media_bot, event, event.get_user_id())
    user_name = (
        user_info.user_remark or user_info.user_displayname or user_info.user_name
    )

    raw_json = json.dumps(
        {"rawtext": [{"text": f"<{user_name}> {process_message(unimsg)}"}]}
    )
    await bds_bot.runcmdEx(f"tellraw @a {raw_json}")


@forward_to_media.handle()
async def _(event: BDSMessageEvent):
    target = Target(config.bds_target_id, config.bds_target_id, True)

    if (media_bot := get_media_bot()) is None:
        return None

    await UniMessage(f"<{event.player.name}> {str(event.message)}").send(
        target, media_bot
    )


@on_notice(priority=10, block=False).handle()
async def join(event: PreJoinEvent):
    target = Target(config.bds_target_id, config.bds_target_id, True)

    if (media_bot := get_media_bot()) is None:
        return None

    await UniMessage(f"{event.player.name} 加入了游戏").send(target, media_bot)


@on_notice(priority=10, block=False).handle()
async def left(event: LeftEvent):
    target = Target(config.bds_target_id, config.bds_target_id, True)

    if (media_bot := get_media_bot()) is None:
        return None

    await UniMessage(f"{event.player.name} 退出了游戏").send(target, media_bot)


@on_notice(priority=10, block=False).handle()
async def die(event: PlayerDieEvent):
    target = Target(config.bds_target_id, config.bds_target_id, True)

    if (media_bot := get_media_bot()) is None:
        return None

    # TODO: 更详细的死亡信息
    await UniMessage(
        (
            f"{event.player.name} 死了"
            if event.source.name is None
            else f"{event.player.name} 因 {event.source.name} 而死"
        )
    ).send(target, media_bot)
