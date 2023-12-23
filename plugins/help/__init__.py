from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

from utils import not_llbds_message_event


plugin_data = {
    "help": {
        "description": "显示帮助信息",
        "usage": {
            "/help": "显示帮助信息",
            "/help 插件名": "显示特定插件的语法和使用示例",
        },
    },
    "whitelist": {
        "description": "白名单管理",
        "usage": {
            "/whitelist add 玩家名": "添加玩家到白名单",
            "/whitelist remove 玩家名": "从白名单移除玩家",
            "/whitelist list": "[AdminOnly] 显示白名单列表",
        },
    },
    "command": {
        "description": "执行指令",
        "usage": {
            "/sudo 指令": "[AdminOnly] 执行指令",
        },
    },
    "list": {
        "description": "显示在线玩家",
        "usage": {
            "/list": "显示在线玩家",
        },
    },
    "forward": {
        "description": "转发消息",
        "usage": {
            "任何消息": "游戏内外消息双向转发",
        },
    },
}


help = on_command("help", rule=not_llbds_message_event, priority=1)


@help.handle()
async def _(plugin: Message = CommandArg()):
    plugin = plugin.extract_plain_text().strip()

    if plugin == "":
        plugin_msg = "\n    ".join(
            [
                f"{plugin_name} {plugin_info['description']}"
                for plugin_name, plugin_info in plugin_data.items()
            ]
        )
        msg = "当前可用的插件有：\n" f"    {plugin_msg}\n" "输入“/help 插件名”查看特定插件的语法和使用示例。"
        await help.finish(msg)
    elif plugin in plugin_data:
        msg = f"插件 {plugin} 可用的指令有：\n    " + "\n    ".join(
            [
                f"{command} -{usage}"
                for command, usage in plugin_data[plugin]["usage"].items()
            ]
        )
        await help.finish(msg)
    else:
        await help.finish("未找到该插件！")
