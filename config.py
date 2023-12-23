from typing import Optional, Union
from pydantic import BaseModel

from nonebot import get_driver


class Config(BaseModel):
    bds_target_id: Optional[Union[int, str]]
    """Bot 回应对象，由平台决定，默认回应所有人"""


def get_config():
    return Config(**get_driver().config.dict())


__all__ = ["get_config"]
