import logging
from plugins.scanner.base_scanner import BaseScanner, ListingItem
from core.evaluator import DealEvaluator
from core.persuasion import PersuasionEngine

logger = logging.getLogger("DonMir.WheelsIntelligence")

class WheelsScanner(BaseScanner):
    def __init__(self, bus):
        super().__init__(bus, name="wheels_scanner")
        self.evaluator = DealEvaluator()
        self.psych = PersuasionEngine()

    def fetch_items(self):
        return [{
            "id": "wheels-v6-001",
            "title": "Литые диски R17 с резиной Continental",
            "price": 400.0,
            "rims_market": 300.0,
            "tire_new_price": 150.0,
            "tread_mm": 3.5, # Критический износ
            "nuances": ["Микротрещины на резине", "Сварка на одном диске"],
            "seller_profile": {"urgency": False}
        }]

    def run_scan(self):
        for raw in self.fetch_items():
            # 1. Математика износа ( DonMir Tread Model )
            tires_value = (raw["tread_mm"] / 8.0) * raw["tire_new_price"] * 4
            market_total = raw["rims_market"] + tires_value
            
            # 2. Анализ маржи
            res = self.evaluator.analyze(raw["price"], market_total, 40.0, 150.0, raw["nuances"])
            
            # 3. Психологическая атака
            # Добавляем кастомный аргумент: "Риск для жизни"
            logic = self.psych.get_strategy("wheels", raw["nuances"] + ["Критический износ протектора"], raw["seller_profile"])

            report = (
                f"\n--- 🛞 DonMir WHEELS INTELLIGENCE ---\n"
                f"ОБЪЕКТ: {raw['title']}\n"
                f"ЗОНА: {res['zone']}\n"
                f"ТОРГ ДО: {res['target_price']}$\n"
                f"--- ОПЕРАТИВНЫЙ СКРИПТ ---\n"
            )
            for t in logic["tactics"]:
                report += f"▶ {t['method']}: {t['phrase']}\n"
            
            logger.info(report)
            self.process_and_publish(ListingItem(id=raw["id"], title=raw["title"], price=raw["price"], url=""))
