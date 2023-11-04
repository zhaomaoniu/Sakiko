from nonebot import get_driver

from BDS import Server


config = get_driver().config
bds_server = Server(getattr(config, "bds_dir"))
