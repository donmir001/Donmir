import logging
from typing import Dict, Any, List, Optional
from plugins.scanner.base_scanner import BaseScanner, ListingItem

logger = logging.getLogger("DonMir.GoldScanner")

class GoldScanner(BaseScanner):
    """
    Интеллектуальный сканер драгметаллов.
    Рассчитывает реальную стоимость изделия исходя из пробы, веса и биржевых котировок.
    """

    def __init__(self, bus):
        super().__init__(bus, name="gold_scanner")
        # Устанавливаем текущую рыночную цену за 1 грамм чистого золота (пример)
        self.spot_price_usd_per_gram = 75.0 

    def fetch_items(self) -> List[Dict[str, Any]]:
        """Имитация парсинга площадок (Kufar, Аукционы, Ломбарды)."""
        return [
            {
                "id": "gold-001",
                "title": "Золотая цепь, 585 проба",
                "weight": 10.5,      # Вес в граммах
                "purity": 0.585,     # Проба
                "price_usd": 350.0,
                "url": "https://kufar.by/item/gold-chain-001",
                "description": "Классическое плетение, состояние идеал"
            }
        ]

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Расчет стоимости лома vs стоимости изделия."""
        try:
            weight = float(raw_item["weight"])
            purity = float(raw_item["purity"])
            asking_price = float(raw_item["price_usd"])

            # Расчет чистой стоимости металла (Metal Value)
            metal_value = weight * purity * self.spot_price_usd_per_gram
            
            # Если цена ниже стоимости чистого металла — это мгновенный сигнал (Deal!)
            if asking_price < metal_value:
                logger.warning(f"🔥 НАЙДЕН МЕТАЛЛ НИЖЕ БИРЖИ: {raw_item['title']}")
            
            return ListingItem(
                id=raw_item["id"],
                title=f"💍 [GOLD {int(purity*1000)}] {raw_item['title']} ({weight}g)",
                price=asking_price,
                estimated_market_price=metal_value * 1.2, # Рыночная цена изделия обычно на 20% выше лома
                url=raw_item["url"],
                category="luxury/gold",
                raw_data=raw_item
            )
        except (KeyError, ValueError) as e:
            logger.error(f"Ошибка анализа золота: {e}")
            return None

    def run_scan(self) -> List[ListingItem]:
        """Запуск глубокого анализа рынка драгметаллов."""
        logger.info("Запуск сканера драгметаллов...")
        raw_items = self.fetch_items()
        deals = []

        for raw in raw_items:
            item = self.parse_item(raw)
            if item:
                self.process_and_publish(item)
                deals.append(item)
        
        return deals
