from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DealEvaluation:
    """Результат финансовой оценки и расчета рисков."""
    item_id: str
    title: str
    price: float
    estimated_market_price: float
    gross_profit: float
    net_profit: float
    profit_margin_percent: float
    risk_level: str  # SAFE, MEDIUM_RISK, HIGH_RISK
    recommendation: str


class DealEvaluator:
    """Модуль расчета рисков, комиссий и выгоды для DonMir Scanner."""

    def __init__(self, platform_fee_percent: float = 5.0, shipping_cost: float = 10.0):
        self.platform_fee_percent = platform_fee_percent
        self.shipping_cost = shipping_cost

    def evaluate(self, item_data: Dict[str, Any]) -> DealEvaluation:
        """Проводит финансовый расчет и оценку рисков по объекту."""
        price = float(item_data.get("price", 0.0))
        market_price = float(item_data.get("estimated_market_price", 0.0))

        # Валовая и чистая прибыль (с учетом комиссии и доставки)
        gross_profit = market_price - price
        fee_amount = market_price * (self.platform_fee_percent / 100.0)
        net_profit = gross_profit - fee_amount - self.shipping_cost

        # Маржинальность в процентах
        profit_margin = (net_profit / market_price * 100.0) if market_price > 0 else 0.0

        # Определение уровня риска и рекомендаций
        if profit_margin >= 20.0:
            risk_level = "SAFE"
            recommendation = "BUY_IMMEDIATELY"
        elif profit_margin >= 10.0:
            risk_level = "MEDIUM_RISK"
            recommendation = "CHECK_CONDITION_AND_BUY"
        else:
            risk_level = "HIGH_RISK"
            recommendation = "PASS_OR_NEGOTIATE"

        return DealEvaluation(
            item_id=item_data.get("id", "unknown"),
            title=item_data.get("title", "Unknown Item"),
            price=price,
            estimated_market_price=market_price,
            gross_profit=round(gross_profit, 2),
            net_profit=round(net_profit, 2),
            profit_margin_percent=round(profit_margin, 2),
            risk_level=risk_level,
            recommendation=recommendation,
        )
