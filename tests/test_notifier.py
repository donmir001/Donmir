import pytest
from core.event_bus import EventBus
from plugins.scanner.evaluator import DealEvaluator
from plugins.scanner.notifier import DealNotifier


def test_deal_notifier_formatting():
    """Тест модуля уведомлений: проверка перехвата событий EventBus и форматирования сообщений."""
    bus = EventBus()
    evaluator = DealEvaluator(platform_fee_percent=5.0, shipping_cost=10.0)
    notifier = DealNotifier(bus=bus, evaluator=evaluator)

    item = {
        "id": "car-001",
        "title": "Toyota Camry 2.5 2021",
        "price": 18000.0,
        "estimated_market_price": 24000.0,
    }

    # Имитируем публикацию события найденной сделки в EventBus
    msg = notifier.handle_deal(item)

    # Проверяем, что текстовая карточка алерта сформирована корректно
    assert "DONMIR DEAL ALERT" in msg
    assert "Toyota Camry 2.5 2021" in msg
    assert "$18,000.00" in msg
    assert "SAFE" in msg
    assert "BUY_IMMEDIATELY" in msg
