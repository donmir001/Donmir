"""
DonMir Boot Agent - Модуль безопасности
Модуль: security/verifier.py
Назначение: Проверка подлинности команд Владельца и прав доступа.
"""

import hmac
import hashlib
from config.settings import settings


class SecurityVerifier:
    """Класс для проверки авторизации и целостности инструкций Владельца."""

    @staticmethod
    def verify_owner_key(provided_key: str) -> bool:
        """Проверяет секретный ключ Владельца."""
        if not provided_key:
            return False
        # Безопасное сравнение строк для защиты от атак по времени
        return hmac.compare_digest(provided_key, settings.OWNER_KEY)

    @staticmethod
    def is_action_allowed(action_name: str) -> bool:
        """Проверяет, разрешено ли действие согласно правилам безопасности."""
        # Запрещенные критические действия
        forbidden_actions = ["delete_system_core", "change_owner_rights"]
        return action_name not in forbidden_actions


# Экземпляр верификатора безопасности
verifier = SecurityVerifier()
