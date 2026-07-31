"""
DonMir Boot Agent - Core Kernel
Главный класс ядра, объединяющий все системные компоненты.
"""

import logging
from typing import Dict, Any, Optional
from config.settings import Settings
from core.constitution import Constitution
from core.dispatcher import Dispatcher
from security.verifier import Verifier

# Настройка базового логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DonMirKernel")


class DonMirKernel:
    """Основное ядро платформы DonMir Boot Agent."""

    def __init__(self):
        logger.info("Initializing DonMir Kernel...")
        self.settings = Settings()
        self.constitution = Constitution()
        self.verifier = Verifier()
        self.dispatcher = Dispatcher()
        logger.info("DonMir Kernel successfully initialized.")

    def execute_command(self, command_name: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Главная точка входа для выполнения команд агентом.
        """
        if payload is None:
            payload = {}

        logger.info(f"Received command: {command_name}")
        
        # Передаем задачу диспетчеру
        result = self.dispatcher.dispatch(command_name, payload)
        
        logger.info(f"Command {command_name} finished with status: {result.get('status')}")
        return result

    def get_status(self) -> Dict[str, Any]:
        """Возвращает текущий статус ядра и системы."""
        return {
            "kernel": "active",
            "environment": self.settings.ENV if hasattr(self.settings, "ENV") else "production",
            "laws_enforced": len(self.constitution.get_all_laws())
        }
