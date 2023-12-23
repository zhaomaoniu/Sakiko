from nonebot import get_driver, on_command
from nonebot.adapters import Event, Message
from nonebot.params import CommandArg

from utils import not_llbds_message_event, get_bds_bot


cmd = on_command("sudo", rule=not_llbds_message_event, block=True, priority=1)


@cmd.handle()
async def _(event: Event, command: Message = CommandArg()):
    if event.get_user_id() not in get_driver().config.superusers:
        await cmd.finish("权限不足！")

    if (bds_bot := get_bds_bot()) is None:
        return None

    cmd_result = await bds_bot.runcmdEx(str(command).strip())
    await cmd.finish(cmd_result["output"] or "已执行，指令无返回值")
