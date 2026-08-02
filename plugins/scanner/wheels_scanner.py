lo
gging
from typing import Dict, Any, List, Optional
from plugins.scanner.base_scanner import BaseScanner, ListingItem
from core.evaluator import DealEvaluator
from core.persuasion import PersuasionEngine

logger = logging.getLogger("DonMir.SupremeWheels")

class WheelsScanner(BaseScanner):
    """Сканер колес и дисков DonMir 100/10."""
    def __init__(self, bus):
        super().__init__(bus, name="wheels_scanner")
        self.evaluator = DealEvaluator()
        self.psych = PersuasionEngine()

    def fetch_items(self) -> List[Dict[str, Any]]:
        return [{
            "id": "w-golf-4", "title": "Диски VW R16 + Continental",
            "price": 400.0, "rims_market": 300.0,
            "tire_new_price": 150.0, "tread_mm": 3.5,
            "nuances": ["Трещины на резине", "Сварка на диске"],
            "seller_profile": {"urgency": False}
        }]

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Этот метод мы добавили, чтобы билд не падал."""
        try:
            return ListingItem(
                id=raw_item["id"], title=raw_item["title"],
                price=float(raw_item["price"]),
                estimated_market_price=float(raw_item["rims_market"] + 200.0),
                url="http://donmir.io", category="wheels", raw_data=raw_item
            )
        
                   except: return Nonе
        def run_scan(self) -> List[ListingItem]:
        processed = []
        for raw in self.fetch_items():
            item = self.parse_item(raw)
            if item:
                val = (raw["tread_mm"]/8.0)*raw["tire_new_price"]*4
                m_total = raw["rims_market"]+val
                res = self.evaluator.analyze(item.price,m_total,40.0,150.0,raw["nuances"])
                intel = self.psych.get_strategy("wheels",raw["nuances"],raw["seller_profile"])
                logger.info(f"WHEELS: {res['zone']} | TARGET: {res['target_price']}$")
                self.process_and_publish(item)
                processed.append(item)
        return processed
