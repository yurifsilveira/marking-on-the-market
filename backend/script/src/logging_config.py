import logging.config
from os import path, makedirs

CONFIG_PATH = path.join(path.dirname(__file__), "logging.config")

makedirs("logs", exist_ok=True)

logging.config.fileConfig(CONFIG_PATH, disable_existing_loggers=False)

logger = logging.getLogger("TesouroDireto")

logger.info("🔧 Logging configurado via logging.config (rotação diária ativa)")
