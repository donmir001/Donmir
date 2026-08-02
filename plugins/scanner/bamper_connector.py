import logging
from plugins.scanner.base_scanner import BaseScanner, ListingItem
from core.evaluator import DealEvaluator
from core.persuasion import PersuasionEngine

logger = logging.getLogger("DonMir.BamperDeepSearch")

class BamperConnector(BaseScanner):
    def __init__(self, bus):
        super().__init__(bus, name="bamper_connector")
        self.evaluator = DealEvaluator()
        self.psych = PersuasionEngine()

    def fetch_items(self):
        return [{
            "id": "b-998877",
            "title": "Турбина Garrett для Opel 1.7 CDTI",
            "price": 350.0,
            "market_price": 500.0,
            "nuances": ["Люфт крыльчатки", "Масло в патрубке", "Нет гарантийного талона"],
            "seller_profile": {"urgency": True}
        }]

    def run_scan(self):
        for raw in self.fetch_items():
            res = self.evaluator.analyze(raw["price"], raw["market_price"], 30.0, 100.0, raw["nuances"])
            logic = self.psych.get_strategy("parts", raw["nuances"], raw["seller_profile"])

            report = (
                f"\n--- 🔧 DonMir DEEP SEARCH: PARTS ---\n"
                f"ОБЪЕКТ: {raw['title']}\n"
                f"СТАТУС: {res['zone']}\n"
                f"ТАКТИКА: {logic['operational_tone']}\n"
                f"--- АРГУМЕНТАЦИЯ MI6 ---\n"
            )
            for t in logic["tactics"]:
                report += f"• {t['phrase']}\n"
            
            report += f"\nЦЕНА ПЕРЕХВАТА: {res['target_price']}$\n"
            
