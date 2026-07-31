import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "DonMir Boot Agent")
    VERSION: str = os.getenv("VERSION", "1.2.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Пути хранилища
    BASE_DIR: Path = BASE_DIR
    STORAGE_DIR: Path = BASE_DIR / "storage"
    LOGS_DIR: Path = STORAGE_DIR / "logs"
    DATA_DIR: Path = STORAGE_DIR / "data"

settings = Settings()
