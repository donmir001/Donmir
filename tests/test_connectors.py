import pytest
from core.event_bus import EventBus
from plugins.scanner.connectors.konfiskat_connector import KonfiskatConnector
from plugins.scanner.connectors.bamper_connector import BamperConnector


def test_konfiskat_connector():
    """Тест сканера Таможенного Конфиската РБ (ТД Восточный)."""
    bus = EventBus()
    connector = KonfiskatConnector(bus)

    items_found = []
    deals_detected = []

    bus.subscribe("scanner:item_found", lambda item: items_found.append(item))
    bus.subscribe("scanner:deal_detected", lambda item: deals_detected.append(item))

    processed = connector.run_scan()

    assert len(processed) == 3
    assert len(items_found) == 3
    # Выгода >= 15% у всех трех лотов конфиската
    assert len(deals_detected) == 3

    titles = [d["title"] for d in deals_detected]
    assert any("BMW 318i" in t for t in titles)
    assert any("Золотое цепь" in t for t in titles)


def test_bamper_connector():
    """Тест сканера автозапчастей Bamper.by (арбитраж редкого руля BMW $20 -> $100)."""
    bus = EventBus()
    connector = BamperConnector(bus)

    items_found = []
    deals_detected = []

    bus.subscribe("scanner:item_found", lambda item: items_found.append(item))
    bus.subscribe("scanner:deal_detected", lambda item: deals_detected.append(item))

    processed = connector.run_scan()

    assert len(processed) == 3
    # Из 3 запчастей выгода >= 15% у Руля BMW ($20 vs $100) и Фары Porsche ($150 vs $450)
    assert len(deals_detected) == 2

    deal_titles = [d["title"] for d in deals_detected]
    assert any("Руль БМВ" in t for t in deal_titles)
    assert any("Фара LED" in t for t in deal_titles)
