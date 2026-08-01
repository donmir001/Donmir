import logging
from core.event_bus import EventBus
from executor.task_runner import TaskRunner
from plugins.scanner.phone_scanner import PhoneScanner
from plugins.scanner.car_scanner import CarScanner

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

    # 2. Настройка обработчиков событий (Notifiers)
    bus.subscribe(
        "scanner:item_found",
        lambda item: logger.info(
            f"[SCANNER] Processed [{item.get('category', 'general')}]: {item['title']} (${item['price']})"
        )
    )
    bus.subscribe(
        "scanner:deal_detected",
        lambda item: logger.warning(
            f"🔥 [DEAL FOUND!] [{item.get('category', 'general')}] {item['title']} | Price: ${item['price']} | Market: ${item['estimated_market_price']}"
        )
    )

    # 3. Инициализация сканеров (Электроника + Автомобили)
    phone_scanner = PhoneScanner(bus)
    car_scanner = CarScanner(bus)

    # 4. Регистрация задач сканирования в TaskRunner
    runner.register_task("scan_phones", phone_scanner.run_scan)
    runner.register_task("scan_cars", car_scanner.run_scan)

    logger.info("DonMir Boot Agent engine initialized successfully.")
    logger.info("Executing tasks: 'scan_phones' and 'scan_cars' via TaskRunner...")

    # 5. Запуск сканирования всех вертикалей
    phone_results = runner.run_task("scan_phones")
    car_results = runner.run_task("scan_cars")

    total_items = len(phone_results) + len(car_results)
    logger.info(f"=== Scan completed. Total items processed: {total_items} (Phones: {len(phone_results)}, Cars: {len(car_results)}) ===")


if __name__ == "__main__":
    main()
