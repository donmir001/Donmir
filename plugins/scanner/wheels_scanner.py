from typing import Dict, Any, List, Optional
from plugins.scanner.base_scanner import BaseScanner, ListingItem

class WheelsScanner(BaseScanner):
    """Сканер автомобильных дисков и шин."""

    def __init__(self, bus, min_profit_usd: float = 100.0):
        super().__init__(bus, name="wheels_scanner")
        self.min_profit_usd = min_profit_usd

    def fetch_items(self) -> List[Dict[str, Any]]:
        # Демо-данные (как в примере с Гольфом)
        return [
            {
                "id": "kufar-wheels-901",
                "title": "Диски VW Golf 4 R16 (Срочно)",
                "price": 90.0,
                "estimated_market_price": 300.0,
                "url": "https://kufar.by/item/wheels-901",
                "category": "wheels"
            }
        ]

    def run_scan(self) -> List[ListingItem]:
        raw_items = self.fetch_items()
        processed = []
        for raw in raw_items:
            profit = raw["estimated_market_price"] - raw["price"]
            if profit >= self.min_profit_usd:
                item = ListingItem(
                    id=raw["id"],
                    title=raw["title"],
                    price=raw["price"],
                    estimated_market_price=raw["estimated_market_price"],
                    url=raw["url"],
                    category=raw["category"],
                    raw_data=raw
                )
                self.process_and_publish(item)
                processed.append(item)
        return processed
