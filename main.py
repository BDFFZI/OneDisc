#!python3
import subprocess
import sys
import os

# 自动安装依赖
if os.path.exists("requirements.txt"):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        import importlib
        importlib.invalidate_caches()
    except Exception as e:
        print(f"[Warning] 自动安装依赖失败: {e}")

from utils.config import config
from utils.client import client
from utils.logger import get_logger, init_logger
from version import VERSION, SUB_VER

init_logger(config["system"].get("logger", {"level": 20}))
logger = get_logger()
logger.info("OneDisc (By: IT Craft Development Team)")
logger.info(f"当前版本：{VERSION}")

# 导入插件
import utils.event.discord_event
import actions.v12.file
import actions.v12.basic
import utils.commands
import actions.v11.basic
import actions.v11.operations

try:
    client.run(config["account_token"], log_handler=None)
except Exception as e:
    logger.critical(f"OneDisc 启动失败: {e}")
    if "Cannot connect to host" in str(e):
        logger.error("检测到连接超时！请检查您的代理设置 (config.json -> system.proxy) 以及代理软件是否正在运行。")
    elif "401" in str(e):
        logger.error("检测到 401 错误！请检查您的 account_token 是否正确。")
    else:
        import traceback
        logger.error(traceback.format_exc())
