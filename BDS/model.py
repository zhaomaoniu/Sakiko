from enum import IntEnum
from typing import TypedDict


class SenderType(IntEnum):
    bds = 0
    bot = 1


class CommandType(IntEnum):
    command = 0
    result = 1


class Payload(TypedDict):
    sender_type: SenderType
    command_type: CommandType
    echo: str
    context: str
