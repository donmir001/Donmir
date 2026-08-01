import logging
import time
from core.event_bus import EventBus
from executor.task_runner import TaskRunner
from plugins.scanner.phone_scanner import PhoneScanner

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
        lambda item: logger.info(f"[SCANNER] Processed: {item['title']} (${item['price']})")
    )
    bus.subscribe(
        "scanner:deal_detected",
        lambda item: logger.warning(
            f"🔥 [DEAL FOUND!] {item['title']} | Price: ${item['price']} | Market: ${item['estimated_market_price']}"
        )
    )

    # 3. Инициализация и регистрация сканера
    scanner = PhoneScanner(bus)
    runner.register_task("scan_phones", scanner.run_scan)

    logger.info("DonMir Boot Agent engine initialized successfully.")
    logger.info("Executing task: 'scan_phones' via TaskRunner...")

    # 4. Запуск задачи сканирования через TaskRunner
    results = runner.run_task("scan_phones")
    logger.info(f"=== Scan completed. Processed items count: {len(results)} ===")


if __name__ == "__main__":
    main()
