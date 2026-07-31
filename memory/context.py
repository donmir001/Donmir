"""
DonMir Boot Agent — Модуль управления контекстной памятью (Context Memory Manager)
Отвечает за хранение, обновление и очистку оперативного контекста агента.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("donmir.memory.context")


class ContextManager:
    """
    Класс управления краткосрочной и оперативной памятью агента DonMir.
    """

    def __init__(self, max_history_size: int = 50):
        self.max_history_size = max_history_size
        self.history: List[Dict[str, Any]] = []
        self.state: Dict[str, Any] = {
            "session_start": datetime.now().isoformat(),
            "active_task": None,
            "variables": {}
        }

    def add_event(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Добавляет новое событие или сообщение в историю контекста.
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self.history.append(event)
        
        # Ограничение размера истории для оптимизации памяти
        if len(self.history) > self.max_history_size:
            self.history.pop(0)

        logger.debug(f"[ContextManager] Добавлено событие от роли '{role}'. Всего событий: {len(self.history)}")

    def set_variable(self, key: str, value: Any) -> None:
        """Сохраняет переменную в текущую сессию."""
        self.state["variables"][key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        """Получает значение переменной сессии."""
        return self.state["variables"].get(key, default)

    def get_full_context(self) -> Dict[str, Any]:
        """Возвращает полный срез контекста для формирования промпта."""
        return {
            "state": self.state,
            "history": self.history
        }

    def clear_history(self) -> None:
        """Очищает историю диалога/выполнения."""
        self.history.clear()
        logger.info("[ContextManager] История контекста очищена.")


# Глобальный экземпляр контекста
context_manager = ContextManager()
