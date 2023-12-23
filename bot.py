import nonebot
from nonebot.adapters.llbds.adapter import Adapter as LLBDSAdapter
from nonebot.adapters.red import Adapter as RedAdapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(LLBDSAdapter)
driver.register_adapter(RedAdapter)

nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run()
