import json
from pathlib import Path

APP_NAME = "DonMir Boot Agent"
CONFIG_PATH = Path("config/config.json")

DEFAULT_CONFIG = {
    "project_name": "DonMir",
    "version": "0.1",
    "mode": "development",
    "data_path": "./storage",
}


def load_config(config_path: Path = CONFIG_PATH) -> dict:
    """Загружает и валидирует файл конфигурации."""
    if not config_path.exists():
        return DEFAULT_CONFIG

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            # Безопасная валидация обязательных полей
            required_keys = ["project_name", "version", "mode", "data_path"]
            for key in required_keys:
                if key not in config:
                    raise KeyError(f"Missing required config key: {key}")
            return config
    except Exception as e:
        print(f"Warning: Config load error ({e}). Using defaults.")
        return DEFAULT_CONFIG


def get_boot_message(config: dict) -> str:
    """Формирует стартовое сообщение Boot Agent."""
    version = config.get("version", "0.1")
    return f"{APP_NAME}\n\nVersion {version}\n\nSystem initialized."


def get_system_info(config: dict) -> str:
    """Формирует информацию о состоянии платформы на основе конфигурации."""
    project = config.get("project_name", "DonMir")
    mode = config.get("mode", "development")
    data_path = config.get("data_path", "./storage")
    return (
        f"Platform started\n"
        f"Project: {project}\n"
        f"Mode: {mode}\n"
        f"Data Path: {data_path}\n"
        f"Status: Ready"
    )


def main() -> None:
    """Точка входа в приложение."""
    config = load_config()
    print(get_boot_message(config))
    print()
    print(get_system_info(config))


if __name__ == "__main__":
    main()
