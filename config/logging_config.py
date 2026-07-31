import logging
import sys
from config.settings import settings

def setup_logging() -> logging.Logger:
    """Настройка централизованной системы логирования DonMir."""
    settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = settings.LOGS_DIR / "agent.log"
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8")
        ]
    )
    
    logger = logging.getLogger("donmir")
    logger.info(f"Logging initialized. Service: {settings.PROJECT_NAME} v{settings.VERSION}")
    return logger
