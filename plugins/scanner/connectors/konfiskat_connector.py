from typing import Dict, Any, List, Optional
from core.event_bus import EventBus
from plugins.scanner.base_scanner import BaseScanner, ListingItem


class KonfiskatConnector(BaseScanner):
    """Коннектор для парсинга Таможенного Конфиската и Аукционов (ТД Восточный, РБ)."""

    def __init__(self, bus: EventBus):
        super().__init__(bus, name="konfiskat_connector")

    def fetch_items(self) -> List[Dict[str, Any]]:
        """Имитация парсинга каталога и аукционов konfiskat.by."""
        return [
            {
                "id": "konfiskat-auto-101",
                "title": "BMW 318i 1994 (Конфискат, Аукцион ТД Восточный)",
                "price": 600.0,  # 1881 BYN
                "estimated_market_price": 1800.0,  # Оценка рынка
                "category": "automotive/cars",
                "country": "BY",
                "city": "Minsk",
                "url": "https://konfiskat.by/auction/lot-21752",
            },
            {
                "id": "konfiskat-gold-102",
                "title": "Лот: Золотое цепь 585 проба (Изъято таможней, Вес 22г)",
                "price": 550.0,
                "estimated_market_price": 990.0,  # Оценка по бирже чистого металла
                "category": "jewelry/gold",
                "country": "BY",
                "city": "Minsk",
                "url": "https://konfiskat.by/catalog/lot-gold-22",
            },
            {
                "id": "konfiskat-tech-103",
                "title": "Apple iPhone 12 Pro Max (Конфискат в заводской упаковке)",
                "price": 300.0,
                "estimated_market_price": 550.0,
                "category": "electronics/phones",
                "country": "BY",
                "city": "Minsk",
                "url": "https://konfiskat.by/catalog/iphone-12-promax",
            },
        ]

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Преобразование лота конфиската в ListingItem."""
        try:
            return ListingItem(
                id=raw_item["id"],
                title=f"🏛️ [КОНФИСКАТ РБ] {raw_item['title']}",
                price=float(raw_item["price"]),
                estimated_market_price=float(raw_item["estimated_market_price"]),
                url=raw_item["url"],
                category=raw_item["category"],
                raw_data=raw_item,
            )
        except (KeyError, ValueError):
            return None

    def run_scan(self) -> List[ListingItem]:
        """Запуск сканирования лотов конфиската."""
        raw_items = self.fetch_items()
        processed_items = []

        for raw in raw_items:
            item = self.parse_item(raw)
            if item:
                self.process_and_publish(item)
                processed_items.append(item)

        return processed_items
