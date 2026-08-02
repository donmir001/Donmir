import logging
import sys
from core.event_bus import EventBus

# Импорт сканеров и коннекторов
from plugins.scanner.phone_scanner import PhoneScanner
from plugins.scanner.car_scanner import CarScanner
from plugins.scanner.gold_scanner import GoldScanner
from plugins.scanner.wheels_scanner import WheelsScanner
from plugins.scanner.konfiskat_connector import KonfiskatConnector
from plugins.scanner.bamper_connector import BamperConnector
from plugins.scanner.notifier import DealNotifier

# Настройка системного журналирования (Logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("DonMirBootAgent")

def main():
    logger.info("--- Запуск DonMir Boot Agent: Инициализация системы ---")

    # 1. Создаем общую шину событий
    bus = EventBus()

    # 2. Подключаем систему уведомлений
    notifier = DealNotifier(bus)

    # 3. Список всех активных сканеров
    scanners = [
        PhoneScanner(bus),
        CarScanner(bus),
        GoldScanner(bus),
        WheelsScanner(bus),
        KonfiskatConnector(bus),
        BamperConnector(bus)
    ]

    logger.info(f"Успешно загружено сканеров: {len(scanners)}")

    # 4. Запуск цикла диагностики (проверка каждого сканера)
    for scanner in scanners:
        logger.info(f"Проверка модуля: {scanner.__class__.__name__}...")
        try:
            scanner.run_scan()
            logger.info(f"Модуль {scanner.__class__.__name__} - OK")
        except Exception as e:
            logger.error(f"Ошибка в модуле {scanner.__class__.__name__}: {e}")
            sys.exit(1)

    logger.info("--- Диагностика завершена успешно! Все системы в норме. ---")

if __name__ == "__main__":
    main()
