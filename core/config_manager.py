import json
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """Менеджер загрузки и доступа к конфигурации агента."""

    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}

    def load_config(self) -> Dict[str, Any]:
        """Загружает и валидирует конфигурационный файл JSON."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Файл конфигурации не найден: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка формата JSON в конфигурации: {e}")

        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """Возвращает значение по ключу из конфигурации."""
        return self._config.get(key, default)
