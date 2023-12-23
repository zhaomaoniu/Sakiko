import nonebot
from nonebot.adapters.llbds.adapter import Adapter as LLBDSAdapter

# 请在这里导入你要使用的适配器，并 register 该适配器

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(LLBDSAdapter)

nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run()
