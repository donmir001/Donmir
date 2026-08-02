import logging
from plugins.scanner.base_scanner import BaseScanner, ListingItem
from core.evaluator import DealEvaluator
from core.persuasion import PersuasionEngine

logger = logging.getLogger("DonMir.SupremeScanner")

class PhoneScanner(BaseScanner):
    def __init__(self, bus):
        super().__init__(bus, name="phone_scanner")
        self.evaluator = DealEvaluator()
        self.psych = PersuasionEngine()

    def fetch_items(self):
        # Реальный сценарий: iPhone 15 Pro, продавец нервничает
        return [{
            "id": "supreme-iph-001",
            "title": "iPhone 15 Pro Max (Срочно)",
            "price": 1000.0,
            "market_price": 1300.0,
            "overheads": 40.0,
            "defects": ["Замятие угла", "Неоригинальный кабель", "Пыль под камерой"],
            "seller_profile": {"urgency": True, "type": "private"}
        }]

    def run_scan(self):
        for raw in self.fetch_items():
            # 1. Аналитика DonMir
            res = self.evaluator.analyze(raw["price"], raw["market_price"], raw["overheads"], 200.0, raw["defects"])
            
            # 2. Оперативная Психология (KGB/Mossad)
            intel = self.psych.get_strategy("phone", raw["defects"], raw["seller_profile"])
            
            report = (
                f"\n--- ⚡️ ОПЕРАТИВНАЯ СВОДКА DonMir 100/10 ---\n"
                f"ОБЪЕКТ: {raw['title']}\n"
                f"СТАТУС: {res['zone']}\n"
                f"ТОН ПЕРЕГОВОРОВ: {intel['operational_tone']}\n"
                f"--- СХЕМЫ ВЛИЯНИЯ ---\n"
            )
            
            for t in intel["tactics"]:
                report += f"[{t['source']}] {t['method']}:\n   ➜ {t['phrase']}\n"
            
            report += f"\nЦЕЛЕВАЯ ЦЕНА ЗАХВАТА: {res['target_price']}$\n"
            
            logger.info(report)
            self.process_and_publish(ListingItem(id=raw["id"], title=raw["title"], price=raw["price"], url=""))
