import platform
from typing import Any, Dict
from core.config_manager import ConfigManager
from core.event_bus import EventBus


class SystemCore:
    """Ядро системы: управление жизненным циклом и сбор системных метрик."""

    def __init__(self, config_manager: ConfigManager = None, event_bus: EventBus = None):
        self.config_manager = config_manager or ConfigManager()
        self.event_bus = event_bus or EventBus()
        self.is_running = False

    def initialize(self) -> None:
        """Инициализация ядра, загрузка конфигурации и публикация события запуска."""
        self.config_manager.load_config()
        self.is_running = True
        self.event_bus.publish("system_started", {"status": "running"})

    def get_system_info(self) -> Dict[str, Any]:
        """Возвращает информацию об операционной системе и агенте."""
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "agent_name": self.config_manager.get("agent_name", "Unknown Agent"),
            "version": self.config_manager.get("version", "0.0.0"),
        }

    def shutdown(self) -> None:
        """Завершение работы ядра и публикация события остановки."""
        self.is_running = False
        self.event_bus.publish("system_shutdown", {"status": "stopped"})
