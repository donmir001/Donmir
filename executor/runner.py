"""
DonMir Boot Agent — Исполнитель команд (Executor Runner)
Отвечает за безопасный запуск внешних скриптов, команд и задач в облачном окружении.
"""

import logging
import subprocess
from typing import Dict, Any, Tuple
from security.verifier import verifier

logger = logging.getLogger("donmir.executor.runner")


class CommandExecutor:
    """
    Класс для безопасного выполнения системных команд и скриптов.
    """

    def __init__(self, timeout: int = 30):
        self.default_timeout = timeout

    def execute_shell(self, command: str, safe_mode: bool = True) -> Tuple[bool, str]:
        """
        Выполняет shell-команду с проверкой безопасности и таймаутом.
        """
        logger.info(f"[Executor] Попытка запуска команды: '{command}'")

        # Дополнительная проверка через модуль верификации
        if safe_mode:
            is_safe, msg = verifier.verify({"command": command})
            if not is_safe:
                logger.error(f"[Executor] Запуск отклонен верификатором: {msg}")
                return False, f"Ошибка безопасности: {msg}"

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.default_timeout
            )
            if result.returncode == 0:
                logger.info("[Executor] Команда выполнена успешно.")
                return True, result.stdout.strip()
            else:
                logger.warning(f"[Executor] Команда завершилась с ошибкой: {result.stderr}")
                return False, result.stderr.strip()

        except subprocess.TimeoutExpired:
            error_msg = f"Таймаут исполнения ({self.default_timeout} сек.) превышен."
            logger.error(f"[Executor] {error_msg}")
            return False, error_msg
        except Exception as e:
            logger.error(f"[Executor] Системная ошибка выполнения: {str(e)}")
            return False, str(e)


# Глобальный экземпляр исполнителя
executor = CommandExecutor()
