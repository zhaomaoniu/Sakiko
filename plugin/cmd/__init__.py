from nonebot import on_command, require
from nonebot.adapters.red import MessageEvent, Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.rule import to_me

require("init")

from plugin.init import bds_server, config


@on_command("/", rule=to_me()).handle()
async def _(matcher: Matcher, event: MessageEvent, message: Message = CommandArg()):
    if event.senderUin not in config.superusers:
        await matcher.finish("权限不足！")

    result = await bds_server.run_cmd(message.extract_plain_text().strip())
    await matcher.finish(result)
