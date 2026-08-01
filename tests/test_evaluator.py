import pytest
from plugins.scanner.evaluator import DealEvaluator


def test_deal_evaluator_safe_deal():
    """Тест высокомаржинальной сделки (уровень риска SAFE)."""
    evaluator = DealEvaluator(platform_fee_percent=5.0, shipping_cost=10.0)

    item = {
        "id": "test-001",
        "title": "iPhone 13 128GB",
        "price": 300.0,
        "estimated_market_price": 500.0,
    }

    result = evaluator.evaluate(item)

    # Рынок 500 - Цена 300 = 200 gross
    # Комиссия 5% (25) + Доставка (10) = 35 расходов
    # Чистая прибыль = 165, маржа = 33%
    assert result.gross_profit == 200.0
    assert result.net_profit == 165.0
    assert result.profit_margin_percent == 33.0
    assert result.risk_level == "SAFE"
    assert result.recommendation == "BUY_IMMEDIATELY"


def test_deal_evaluator_high_risk():
    """Тест низкомаржинальной сделки с высоким риском (HIGH_RISK)."""
    evaluator = DealEvaluator(platform_fee_percent=5.0, shipping_cost=10.0)

    item = {
        "id": "test-002",
        "title": "Low Profit Phone",
        "price": 100.0,
        "estimated_market_price": 105.0,
    }

    result = evaluator.evaluate(item)

    assert result.risk_level == "HIGH_RISK"
    assert result.recommendation == "PASS_OR_NEGOTIATE"
