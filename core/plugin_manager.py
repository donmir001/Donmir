import importlib
import logging
from pathlib import Path
from typing import Any, Dict, List


class PluginManager:
    """Менеджер для поиска и динамической загрузки плагинов и модулей."""

    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.loaded_plugins: Dict[str, Any] = {}

    def discover_plugins(self) -> List[str]:
        """Сканирует директорию плагинов и возвращает список доступных модулей."""
        if not self.plugins_dir.exists():
            return []

        plugin_names = []
        for file in self.plugins_dir.glob("*.py"):
            if not file.name.startswith("__"):
                plugin_names.append(file.stem)
        return plugin_names

    def load_plugin(self, plugin_name: str) -> Any:
        """Динамически импортирует плагин по его имени."""
        try:
            module_path = f"{self.plugins_dir.name}.{plugin_name}"
            module = importlib.import_module(module_path)
            self.loaded_plugins[plugin_name] = module
            logging.info(f"Плагин '{plugin_name}' успешно загружен.")
            return module
        except Exception as e:
            logging.error(f"Ошибка при загрузке плагина '{plugin_name}': {e}")
            raise ValueError(f"Не удалось загрузить плагин '{plugin_name}': {e}")
