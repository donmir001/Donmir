import logging
from typing import Dict, Any
from core.event_bus import EventBus
from plugins.scanner.evaluator import DealEvaluator, DealEvaluation

logger = logging.getLogger("DonMirNotifier")


class DealNotifier:
    """Модуль форматирования и рассылки уведомлений о найденных сделках."""

    def __init__(self, bus: EventBus, evaluator: DealEvaluator = None):
        self.bus = bus
        self.evaluator = evaluator or DealEvaluator()
        # Автоматическая подписка на события обнаружения выгодных сделок
        self.bus.subscribe("scanner:deal_detected", self.handle_deal)

    def format_message(self, evaluation: DealEvaluation) -> str:
        """Формирование карточки сделки с финансовым отчетом."""
        risk_emoji = "🛡️" if evaluation.risk_level == "SAFE" else "⚠️"
        return (
            f"\n🔥 ==================== DONMIR DEAL ALERT ====================\n"
            f"📌 Товар: {evaluation.title}\n"
            f"💵 Цена продавца: ${evaluation.price:,.2f}\n"
            f"📊 Рыночная цена: ${evaluation.estimated_market_price:,.2f}\n"
            f"💰 Чистая прибыль: ${evaluation.net_profit:,.2f} ({evaluation.profit_margin_percent}%)\n"
            f"{risk_emoji} Уровень риска: {evaluation.risk_level} | Рекомендация: {evaluation.recommendation}\n"
            f"============================================================"
        )

    def handle_deal(self, item_data: Dict[str, Any]) -> str:
        """Обработка события сделки из EventBus: оценка и публикация алерта."""
        evaluation = self.evaluator.evaluate(item_data)
        message = self.format_message(evaluation)
        logger.warning(message)
        return message
