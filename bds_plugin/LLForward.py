import hashlib
import json
from pathlib import Path
from llpy import ll, mc, Player, Entity

ll.registerPlugin("Forward", "转发事件", [0, 0, 1], {"author": "zhaomaoniu"})


cmd_dir = Path.cwd() / "connect"


def calculate_md5(input_string: str):
    md5 = hashlib.md5()
    md5.update(input_string.encode("utf-8"))
    return md5.hexdigest()


def _getattr(obj: object, name: str, default=None):
    if hasattr(obj, name):
        return getattr(obj, name)
    else:
        return default


def _send(data: dict):
    context = json.dumps(data)
    payload = {
        "sender_type": 0,
        "command_type": 0,
        "echo": "",
        "context": context,
    }

    (cmd_dir / f"b-s-{calculate_md5(context)}.txt").write_text(json.dumps(payload), "UTF-8")


def to_dict(obj: object) -> dict:
    return {
        "name": _getattr(obj, "name"),
    }


def onJoin(player: Player):
    _send(
        {"type": "onJoin", "data": {"player": to_dict(player)}},
    )


def onLeft(player: Player):
    _send(
        {"type": "onLeft", "data": {"player": to_dict(player)}},
    )


def onPlayerDie(player: Player, source: Entity):
    _send(
        {
            "type": "onPlayerDie",
            "data": {"player": to_dict(player), "source": to_dict(source)},
        },
    )


def onChat(player: Player, msg: str):
    _send(
        {"type": "onChat", "data": {"player": to_dict(player), "msg": msg}},
    )


mc.listen("onJoin", onJoin)
mc.listen("onLeft", onLeft)
mc.listen("onPlayerDie", onPlayerDie)
mc.listen("onChat", onChat)
