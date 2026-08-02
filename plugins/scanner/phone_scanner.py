import logging
from typing import Dict, Any, List, Optional
from plugins.scanner.base_scanner import BaseScanner, ListingItem
from core.evaluator import DealEvaluator
from core.persuasion import PersuasionEngine

logger = logging.getLogger("DonMir.SupremePhoneScanner")

class PhoneScanner(BaseScanner):
    """
    Интеллектуальный сканер электроники.
    Единство технического анализа и когнитивного доминирования.
    """
    def __init__(self, bus):
        super().__init__(bus, name="phone_scanner")
        self.evaluator = DealEvaluator()
        self.psych = PersuasionEngine()

    def fetch_items(self) -> List[Dict[str, Any]]:
        """Получение сырых данных (имитация парсинга)."""
        return [{
            "id": "supreme-iph-001",
            "title": "iPhone 15 Pro Max (Срочно)",
            "price": 1000.0,
            "market_price": 1300.0,
            "overheads": 40.0,
            "defects": ["Замятие угла", "Неоригинальный кабель", "Пыль под камерой"],
            "seller_profile": {"urgency": True}
        }]

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Обязательный метод трансформации данных для ядра DonMir."""
        try:
            return ListingItem(
                id=raw_item["id"],
                title=raw_item["title"],
                price=float(raw_item["price"]),
                estimated_market_price=float(raw_item["market_price"]),
                url="",
                category="electronics/phones",
                raw_data=raw_item
            )
        except (KeyError, ValueError):
            return None

    def run_scan(self) -> List[ListingItem]:
        """Запуск глубокого сканирования с выдачей оперативной сводки."""
        raw_items = self.fetch_items()
        processed = []

        for raw in raw_items:
            item = self.parse_item(raw)
            if item:
                # 1. Аналитика DonMir
                res = self.evaluator.analyze(
                    item.price, item.estimated_market_price, 
                    raw["overheads"], 200.0, raw["defects"]
                )
                
                # 2. Психология влияния (КГБ/Моссад/ФБР)
                intel = self.psych.get_strategy("phone", raw["defects"], raw["seller_profile"])
                
                report = (
                    f"\n--- ⚡️ ОПЕРАТИВНАЯ СВОДКА DonMir 100/10 ---\n"
                    f"ОБЪЕКТ: {item.title}\n"
                    f"СТАТУС: {res['zone']}\n"
                    f"ТОН ПЕРЕГОВОРОВ: {intel['operational_tone']}\n"
                    f"--- СХЕМЫ ВЛИЯНИЯ ---\n"
                )
                for t in intel["tactics"]:
                    report += f"[{t['source']}] {t['method']}:\n   ➜ {t['phrase']}\n"
                
                report += f"\nЦЕЛЕВАЯ ЦЕНА ЗАХВАТА: {res['target_price']}$\n"
                
                logger.info(report)
                self.process_and_publish(item)
                processed.append(item)
        
        return processed
