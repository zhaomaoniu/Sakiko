# Sakiko
✨ 基于 NoneBot2 和 LiteLoaderBDS 的 Minecraft 基岩版 Bot ✨

## 概览
Sakiko 是一个用于将 NoneBot2 对接 LiteLoaderBDS 的 Minecraft 基岩版 Bot，实现了 群服互通、增改白名单、执行指令 的功能，提供了在 NoneBot2 内与 BDS 通讯的简便方法。
> 目前仅支持 RedAdapter，未来会替换为 Satori 或 saa + alc 以实现多平台适配

> Sakiko 其实是 BanG Dream! It's MyGO!!!!! 中出现的角色：丰川祥子，被观众称为 客服小祥。在本项目中承担着 BDS 和 NoneBot2 的客服工作（

## 部署
1. 克隆仓库到本地
2. 配置 `.env` 文件：   
   `SUPERUSERS`(可选): 超级用户可以借由 Sakiko 执行指令   
   `BDS_GROUP`(必填): Sakiko 服务的群聊   
   `BDS_DIR`(必填): BDS 所在的目录   
3. 配置 LiteLoaderBDS: 参考[此处](https://docs.litebds.com/zh-Hans/#/README)   
   配置完成后，你还需要将本仓库 bds_plugin 文件夹 中的 `LLCommandIn.py` 与 `LLForward.py` 移动到 BDS 的 plugin 文件夹中
4. 配置 RedAdapter: 参考[此处](https://github.com/nonebot/adapter-red)
> 请确保按照提示正确配置 `.env` 文件
5. 安装环境：
> 推荐在虚拟环境中进行操作

   在命令行中执行 `pip install nonebot2[aiohttp,websockets] nonebot-adapter-red apscheduler`

6. 客服小祥，启动！  
   在 Sakiko 文件夹下运行: `python bot.py`

如果一切正常，启动后不应该报错。有疑问可以加 QQ 群咨询 Staff Z: 666808414

## 拓展
如果你不满足于 Sakiko 现有的功能，可以尝试自己编写插件

一个简单的 Sakiko 插件示例如下
```python
from nonebot import on_command, require
from nonebot.matcher import Matcher

require("init")

from plugin.init import bds_server


@on_command("查服").handle()
async def _(matcher: Matcher):
    result = await bds_server.run_cmd("/list")
    await matcher.finish(result)
```
这个插件实现了一个基础的查服功能，使玩家能够在聊天平台上获取服务器的在线玩家

## 致谢
[kumoSleeping](https://github.com/kumoSleeping): 提供了群服互通的实现方法，命名了 SakikoBot
