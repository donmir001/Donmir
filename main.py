import logging
from core.event_bus import EventBus
from executor.task_runner import TaskRunner

# Импорт сканеров и коннекторов
from plugins.scanner.phone_scanner import PhoneScanner
from plugins.scanner.car_scanner import CarScanner
from plugins.scanner.gold_scanner import GoldScanner
from plugins.scanner.connectors.konfiskat_connector import KonfiskatConnector
from plugins.scanner.connectors.bamper_connector import BamperConnector
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

    # 3. Логирование общей обработки каждого товара
    bus.subscribe(
        "scanner:item_found",
        lambda item: logger.info(
            f"[SCANNER] Processed [{item.get('category', 'general')}]: {item['title']} (${item['price']})"
        )
    )

    # 4. Инициализация всех 5 сканеров и коннекторов
    phone_scanner = PhoneScanner(bus)
    car_scanner = CarScanner(bus)
    gold_scanner = GoldScanner(bus)
    konfiskat_connector = KonfiskatConnector(bus)
    bamper_connector = BamperConnector(bus)

    # 5. Регистрация задач сканирования в TaskRunner
    runner.register_task("scan_phones", phone_scanner.run_scan)
    runner.register_task("scan_cars", car_scanner.run_scan)
    runner.register_task("scan_gold", gold_scanner.run_scan)
    runner.register_task("scan_konfiskat", konfiskat_connector.run_scan)
    runner.register_task("scan_bamper", bamper_connector.run_scan)

    logger.info("DonMir Boot Agent engine initialized successfully.")
    logger.info("Executing 5 scanner tasks: Phones, Cars, Gold, Konfiskat, Bamper...")

    # 6. Запуск всех 5 сканеров
    phone_res = runner.run_task("scan_phones")
    car_res = runner.run_task("scan_cars")
    gold_res = runner.run_task("scan_gold")
    konfiskat_res = runner.run_task("scan_konfiskat")
    bamper_res = runner.run_task("scan_bamper")

    total_items = len(phone_res) + len(car_res) + len(gold_res) + len(konfiskat_res) + len(bamper_res)
    logger.info(f"=== Scan completed. Total items processed across 5 verticals: {total_items} ===")


if __name__ == "__main__":
    main()
