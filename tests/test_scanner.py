import pytest
from core.event_bus import EventBus
from plugins.scanner.phone_scanner import PhoneScanner


def test_phone_scanner_deals_detection():
    """Тест сканера телефонов: проверка работы EventBus и фильтрации выгодных сделок."""
    bus = EventBus()
    scanner = PhoneScanner(bus)

    items_found = []
    deals_detected = []

    # Подписываемся на события сканера в шине EventBus
    bus.subscribe("scanner:item_found", lambda data: items_found.append(data))
    bus.subscribe("scanner:deal_detected", lambda data: deals_detected.append(data))

    # Запускаем сканирование
    processed = scanner.run_scan()

    # 1. Проверяем, что обработано ровно 3 товара
    assert len(processed) == 3
    assert len(items_found) == 3

    # 2. Проверяем, что шина поймала ровно 2 выгодные сделки (iPhone 13 и iPhone 14 Pro)
    assert len(deals_detected) == 2

    # 3. Проверяем заголовки найденных выгодных сделок
    deal_titles = [d["title"] for d in deals_detected]
    assert "iPhone 13 128GB Black" in deal_titles
    assert "iPhone 14 Pro 256GB Gold" in deal_titles
    assert "Samsung Galaxy S22 256GB" not in deal_titles
