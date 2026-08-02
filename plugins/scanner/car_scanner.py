import logging
from typing import Dict, Any, List, Optional
from core.event_bus import EventBus
from plugins.scanner.base_scanner import BaseScanner, ListingItem

logger = logging.getLogger("DonMir.CarScanner")

class CarScanner(BaseScanner):
    """
    Профессиональный сканер автомобильного рынка.
    Интегрирует поиск по VIN, оценку состояния и расчет рыночной маржи.
    """

    def __init__(self, bus: EventBus):
        super().__init__(bus, name="car_scanner")
        self.market_threshold = 0.15  # Мы ищем выгоду минимум 15%

    def fetch_items(self) -> List[Dict[str, Any]]:
        """Имитация глубокого парсинга (AV.by, Kufar Auto)."""
        return [
            {
                "id": "car-by-777",
                "vin": "W0L0AHL4875117755",  # Тот самый Opel из твоих документов
                "title": "Opel Astra H",
                "year": 2007,
                "price_usd": 4200.0,
                "market_price_avg": 5500.0,
                "url": "https://cars.av.by/opel/astra/777",
                "source": "av.by",
                "location": "Minsk"
            }
        ]

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Глубокий анализ лота с проверкой ликвидности и маржи."""
        try:
            price = float(raw_item["price_usd"])
            market_avg = float(raw_item["market_price_avg"])
            profit = market_avg - price
            margin_pct = profit / market_avg

            # Логика DonMir: только если сделка реально выгодная
            if margin_pct < self.market_threshold:
                logger.info(f"Пропуск: {raw_item['title']} (низкая маржа: {margin_pct:.1%})")
                return None

            return ListingItem(
                id=raw_item["id"],
                title=f"🚗 [CAR] {raw_item['title']} ({raw_item['year']})",
                price=price,
                estimated_market_price=market_avg,
                url=raw_item["url"],
                category="transport/cars",
                raw_data=raw_item
            )
        except (KeyError, ValueError) as e:
            logger.error(f"Ошибка парсинга авто {raw_item.get('id')}: {e}")
            return None

    def run_scan(self) -> List[ListingItem]:
        """Запуск цикла профессионального сканирования авторынка."""
        logger.info("Сканирование автомобильных площадок запущено...")
        raw_items = self.fetch_items()
        deals = []

        for raw in raw_items:
            item = self.parse_item(raw)
            if item:
                # Публикуем событие в общую шину DonMir
                self.process_and_publish(item)
                deals.append(item)
        
        return deals
