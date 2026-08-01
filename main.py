import logging
from core.event_bus import EventBus
from executor.task_runner import TaskRunner
from plugins.scanner.phone_scanner import PhoneScanner
from plugins.scanner.car_scanner import CarScanner
from plugins.scanner.notifier import DealNotifier

# Настройка системного журналирования (Logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("DonMirBootAgent")


def main():
    logger.info("=== Starting DonMir Boot Agent v0.2 ===")

    # 1. Инициализация ядра и шины событий
    bus = EventBus()
    runner = TaskRunner(bus)

    # 2. Инициализация модуля алертов и нотификаций
    notifier = DealNotifier(bus)

    # 3. Настройка логирования обработки каждого товара
    bus.subscribe(
        "scanner:item_found",
        lambda item: logger.info(
            f"[SCANNER] Processed [{item.get('category', 'general')}]: {item['title']} (${item['price']})"
        )
    )

    # 4. Инициализация сканеров вертикалей (Электроника + Автомобили)
    phone_scanner = PhoneScanner(bus)
    car_scanner = CarScanner(bus)

    # 5. Регистрация задач сканирования в TaskRunner
    runner.register_task("scan_phones", phone_scanner.run_scan)
    runner.register_task("scan_cars", car_scanner.run_scan)

    logger.info("DonMir Boot Agent engine initialized successfully.")
    logger.info("Executing tasks: 'scan_phones' and 'scan_cars' via TaskRunner...")

    # 6. Запуск сканирования всех вертикалей
    phone_results = runner.run_task("scan_phones")
    car_results = runner.run_task("scan_cars")

    total_items = len(phone_results) + len(car_results)
    logger.info(
        f"=== Scan completed. Total items processed: {total_items} (Phones: {len(phone_results)}, Cars: {len(car_results)}) ==="
    )


if __name__ == "__main__":
    main()
