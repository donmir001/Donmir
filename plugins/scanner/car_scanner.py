from typing import Dict, Any, List, Optional
from core.event_bus import EventBus
from plugins.scanner.base_scanner import BaseScanner, ListingItem


class CarScanner(BaseScanner):
    """Сканер объявлений автомобильного рынка (Автомобильная вертикаль DonMir Scanner)."""

    def __init__(self, bus: EventBus):
        super().__init__(bus, name="car_scanner")

    def fetch_items(self) -> List[Dict[str, Any]]:
        """Имитация получения объявлений по авторынку (демо-данные для тестов и MVP)."""
        return [
            {
                "id": "car-001",
                "title": "Toyota Camry 2.5 2021 (VIN: JTDKN3AU...)",
                "price": 18000.0,
                "estimated_market_price": 24000.0,  # Выгода > 15% (Горячая сделка!)
                "mileage_km": 45000,
                "url": "https://example.com/item/car-001",
            },
            {
                "id": "car-002",
                "title": "BMW 3 Series 2019 (High mileage)",
                "price": 22000.0,
                "estimated_market_price": 23000.0,  # Выгода < 15%
                "mileage_km": 120000,
                "url": "https://example.com/item/car-002",
            },
            {
                "id": "car-003",
                "title": "Porsche Macan S 2020",
                "price": 42000.0,
                "estimated_market_price": 55000.0,  # Выгода > 15% (Горячая сделка!)
                "mileage_km": 30000,
                "url": "https://example.com/item/car-003",
            },
        ]

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Преобразование сырых данных автомобиля в ListingItem."""
        try:
            return ListingItem(
                id=raw_item["id"],
                title=raw_item["title"],
                price=float(raw_item["price"]),
                estimated_market_price=float(raw_item["estimated_market_price"]),
                url=raw_item["url"],
                category="automotive/cars",
                raw_data=raw_item,
            )
        except (KeyError, ValueError):
            return None

    def run_scan(self) -> List[ListingItem]:
        """Запуск автосканирования и публикация событий в EventBus."""
        raw_items = self.fetch_items()
        processed_items = []

        for raw in raw_items:
            item = self.parse_item(raw)
            if item:
                self.process_and_publish(item)
                processed_items.append(item)

        return processed_items
