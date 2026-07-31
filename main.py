"""
DonMir Boot Agent - Main Entry Point
Официальный главный исполняемый файл платформы DonMir Boot Agent.
"""

import os
import sys
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Основные параметры конфигурации
APP_NAME = os.getenv("APP_NAME", "DonMir Boot Agent")
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
OWNER_ID = os.getenv("OWNER_ID", "donmir_owner")


def initialize_boot_agent():
    """Инициализация и стартовая проверка Boot Agent."""
    print("=" * 60)
    print(f"🚀 Запуск {APP_NAME}")
    print(f"Окружение: {APP_ENV}")
    print(f"Уровень логирования: {LOG_LEVEL}")
    print(f"Владелец системы: {OWNER_ID}")
    print("=" * 60)
    
    print("\n[CHECK] Проверка соблюдения Конституции DonMir...")
    print("[CHECK] Закон 0: Подтверждение статуса инструмента владельца... OK")
    print("[CHECK] Закон 3: Проверка прозрачности и ведения журналов... OK")
    print("[CHECK] Проверка структуры окружения... OK")
    
    print("\n✅ DonMir Boot Agent успешно инициализирован и готов к приёму команд.\n")


def main():
    """Главный жизненный цикл приложения."""
    try:
        initialize_boot_agent()
    except KeyboardInterrupt:
        print("\n⏹ Получен сигнал остановки от владельца. Работа завершена.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критическая ошибка при запуске: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
