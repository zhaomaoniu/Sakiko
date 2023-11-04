import json
import hashlib
from pathlib import Path
from llpy import mc, ll, setInterval

ll.registerPlugin("CommandIn", "接收并执行指令", [0, 0, 1], {"author": "zhaomaoniu"})

cmd_dir = Path.cwd() / "connect"


def calculate_md5(input_string: str):
    md5 = hashlib.md5()
    md5.update(input_string.encode("utf-8"))
    return md5.hexdigest()


def init():
    cmd_dir.mkdir(exist_ok=True)


def handle_cmd():
    cmds = [item for item in cmd_dir.iterdir() if item.is_file()]
    for cmd in cmds:
        payload = json.loads(cmd.read_text())
        if payload["command_type"] == 0 and payload["sender_type"] == 1:
            result = mc.runcmdEx(payload["context"])
            cmd.unlink()
            return_payload = {
                "sender_type": 0,
                "command_type": 1,
                "echo": payload["echo"],
                "context": result["output"],
            }
            (cmd_dir / f"b-r-{calculate_md5(payload['echo'])}.txt").write_text(
                json.dumps(return_payload), "UTF-8"
            )
    return 0


mc.listen("onServerStarted", init)

setInterval(handle_cmd, 50)
