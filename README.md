# Sakiko
✨ 基于 NoneBot2 和 LiteLoaderBDS 的 Minecraft 基岩版多平台 Bot ✨

## 概览
Sakiko 是一个用于将 NoneBot2 对接 LiteLoaderBDS 的 Minecraft 基岩版 Bot，实现了 群服互通、增改白名单、执行指令 的功能
> Sakiko 其实是 BanG Dream! It's MyGO!!!!! 中出现的角色：丰川祥子，被观众称为客服小祥。在本项目中承担着 BDS 和 NoneBot2 的客服工作（

## 部署
1. 克隆仓库到本地
2. 配置 `.env` 文件：   
   `BDS_TARGET_ID`(必填): Sakiko 服务的对象，由对接的平台决定   
   `SUPERUSERS`(可选): 超级用户可以借由 Sakiko 执行指令   
3. 配置 LiteLoaderBDS: 参考 [此处](https://docs.litebds.com/zh-Hans/#/README)   
4. 配置 NoneBot Adapter LLBDS: 参考 [此处](https://github.com/zhaomaoniu/nonebot-adapter-llbds)
5. 配置一个 NoneBot Adapter LLBDS 以外的适配器以对接平台
> 请确保按照提示正确配置 `.env` 文件
5. 安装环境：
> 推荐在虚拟环境中进行操作
> 请确保已更新 pip 到最新版本

   在命令行中执行 `pip install -r requirements.txt`

6. 客服小祥，启动！  
   在 Sakiko 文件夹下运行: `python bot.py`

当然，上述步骤仅作为一个示例，如果你有更习惯的部署方法，并确认自己不会弄错什么，就不必拘束于上述步骤   

如果一切正常，启动后不应该报错。有疑问可以加 QQ 群咨询 Staff Z: 666808414

## 拓展
如果你不满足于 Sakiko 现有的功能，可以尝试自己编写插件

这里推荐通过阅读 Sakiko/plugins 中的插件源码 或 查看 NoneBot Adapter LLBDS 的示例插件以及你所使用的适配器的示例插件 来进行编写

## 致谢
[kumoSleeping](https://github.com/kumoSleeping): ~~提供了群服互通的实现方法~~，命名了 SakikoBot
