import logging
import sys
from core.event_bus import EventBus
from executor.task_runner import TaskRunner

# Базовая конфигурация логов
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("DonMirBootAgent")

def main():
    logger.info("--- СИСТЕМА DONMIR: ЗАПУСК ДИАГНОСТИКИ ---")
    
    bus = EventBus()
    runner = TaskRunner(bus)

    # ДИНАМИЧЕСКАЯ ЗАГРУЗКА (Защищенный режим)
    try:
        from plugins.scanner.wheels_scanner import WheelsScanner
        scanner = WheelsScanner(bus)
        runner.register_task("scan_wheels", scanner.run_scan)
        logger.info("✅ Модуль WheelsScanner: ПОДКЛЮЧЕН")
    except Exception as e:
        logger.error(f"❌ Модуль WheelsScanner: ОШИБКА (Пропуск) -> {e}")

    logger.info("--- ДИАГНОСТИКА ЗАВЕРШЕНА: СИСТЕМА СТАБИЛЬНА ---")

if __name__ == 
