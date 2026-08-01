from typing import Dict, Any, List, Optional
from core.event_bus import EventBus
from plugins.scanner.base_scanner import BaseScanner, ListingItem


class PhoneScanner(BaseScanner):
    """Сканер объявлений по смартфонам (MVP вертикали электроники)."""

    def __init__(self, bus: EventBus):
        super().__init__(bus, name="phone_scanner")

    def fetch_items(self) -> List[Dict[str, Any]]:
        """Имитация получения объявлений (демо-данные для тестов и MVP)."""
        return [
            {
                "id": "phone-001",
                "title": "iPhone 13 128GB Black",
                "price": 320.0,
                "estimated_market_price": 450.0,  # Выгода > 15% (Сделка!)
                "url": "https://example.com/item/phone-001",
            },
            {
                "id": "phone-002",
                "title": "Samsung Galaxy S22 256GB",
                "price": 400.0,
                "estimated_market_price": 420.0,  # Маленькая выгода (< 15%)
                "url": "https://example.com/item/phone-002",
            },
            {
                "id": "phone-003",
                "title": "iPhone 14 Pro 256GB Gold",
                "price": 600.0,
                "estimated_market_price": 850.0,  # Выгода > 15% (Сделка!)
                "url": "https://example.com/item/phone-003",
            },
        ]

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Преобразование сырых данных в модель ListingItem."""
        try:
            return ListingItem(
                id=raw_item["id"],
                title=raw_item["title"],
                price=float(raw_item["price"]),
                estimated_market_price=float(raw_item["estimated_market_price"]),
                url=raw_item["url"],
                category="electronics/phones",
                raw_data=raw_item,
            )
        except (KeyError, ValueError):
            return None

    def run_scan(self) -> List[ListingItem]:
        """Запуск цикла сканирования и отправка событий в EventBus."""
        raw_items = self.fetch_items()
        processed_items = []

        for raw in raw_items:
            item = self.parse_item(raw)
            if item:
                self.process_and_publish(item)
                processed_items.append(item)

        return processed_items
