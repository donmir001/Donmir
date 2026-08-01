from typing import Dict, Any, List, Optional
from core.event_bus import EventBus
from plugins.scanner.base_scanner import BaseScanner, ListingItem


class BamperConnector(BaseScanner):
    """Коннектор для парсинга авто- и мотозапчастей с Bamper.by (Беларусь)."""

    def __init__(self, bus: EventBus):
        super().__init__(bus, name="bamper_connector")

    def fetch_items(self) -> List[Dict[str, Any]]:
        """Имитация парсинга каталога авторазборок и частников на Bamper.by."""
        return [
            {
                "id": "bamper-part-001",
                "title": "Руль БМВ б/у (M-Sport с лепестками, недооценка)",
                "price": 20.0,  # Продавец поставил $20, не зная ценности
                "estimated_market_price": 100.0,  # Реальная цена рынка (Allegro/Avito/eBay)
                "category": "auto_parts/steering",
                "country": "BY",
                "city": "Minsk",
                "url": "https://bamper.by/zapchast/ruil-bmw/001",
            },
            {
                "id": "bamper-part-002",
                "title": "Фара LED адаптивная Porsche Cayenne 2018",
                "price": 150.0,
                "estimated_market_price": 450.0,  # Оценка рынка
                "category": "auto_parts/lighting",
                "country": "BY",
                "city": "Grodno",
                "url": "https://bamper.by/zapchast/fara-porsche/002",
            },
            {
                "id": "bamper-part-003",
                "title": "Обычное крыло VW Golf 4 (Без выгоды)",
                "price": 30.0,
                "estimated_market_price": 32.0,
                "category": "auto_parts/body",
                "country": "BY",
                "city": "Brest",
                "url": "https://bamper.by/zapchast/krylo-vw/003",
            },
        ]

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Преобразование запчасти с Bamper.by в ListingItem."""
        try:
            return ListingItem(
                id=raw_item["id"],
                title=f"🔧 [BAMPER.BY] {raw_item['title']}",
                price=float(raw_item["price"]),
                estimated_market_price=float(raw_item["estimated_market_price"]),
                url=raw_item["url"],
                category=raw_item["category"],
                raw_data=raw_item,
            )
        except (KeyError, ValueError):
            return None

    def run_scan(self) -> List[ListingItem]:
        """Запуск сканирования автозапчастей."""
        raw_items = self.fetch_items()
        processed_items = []

        for raw in raw_items:
            item = self.parse_item(raw)
            if item:
                self.process_and_publish(item)
                processed_items.append(item)

        return processed_items
