"""
DonMir Boot Agent — Главный логический агент (Core Agent)
Связывает конфигурацию, верификацию, конституцию и контекстную память.
"""

import logging
from typing import Dict, Any, Tuple
from config.settings import settings
from security.verifier import verifier
from core.constitution import Constitution
from memory.context import context_manager

logger = logging.getLogger("donmir.core.agent")


class DonMirAgent:
    """
    Основной класс Агента DonMir.
    """

    def __init__(self):
        self.name = settings.APP_NAME
        self.version = settings.VERSION
        self.constitution = Constitution
        self.memory = context_manager
        self.verifier = verifier

    def process_command(self, command: str, payload: Dict[str, Any]) -> Tuple[bool, str, Any]:
        """
        Обрабатывает входящую команду от Стратега или системы:
        1. Записывает событие в контекст.
        2. Проверяет действие по Конституции DonMir.
        3. Верифицирует безопасность.
        4. Исполняет логику.
        """
        logger.info(f"[{self.name}] Получена команда: '{command}'")
        
        # 1. Запись в оперативную память
        self.memory.add_event(role="strategist", content=command, metadata=payload)

        # 2. Проверка по Конституции (Законы 0-12)
        law_ok = self.constitution.validate_action(payload)
        if not law_ok:
            error_msg = f"Команда '{command}' заблокирована Конституцией DonMir!"
            logger.warning(error_msg)
            self.memory.add_event(role="agent", content=error_msg)
            return False, error_msg, None

        # 3. Верификация безопасности
        is_safe, sec_msg = self.verifier.verify(payload)
        if not is_safe:
            logger.error(f"Блокировка безопасности: {sec_msg}")
            self.memory.add_event(role="agent", content=sec_msg)
            return False, sec_msg, None

        # 4. Исполнение команды
        response_msg = f"Команда '{command}' успешно принята и обработана Агентом {self.name} v{self.version}."
        self.memory.add_event(role="agent", content=response_msg)
        
        return True, response_msg, {"status": "success", "command": command}


# Глобальный экземпляр Агента
boot_agent = DonMirAgent()
