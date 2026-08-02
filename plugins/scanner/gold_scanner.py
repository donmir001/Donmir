import logging
from plugins.scanner.base_scanner import BaseScanner, ListingItem
from core.evaluator import DealEvaluator

logger = logging.getLogger("DonMir.GoldScanner")

class GoldScanner(BaseScanner):
    """
    Интеллектуальный арбитраж драгметаллов.
    Синхронизирует цену изделия с мировой ценой лома (Spot Price).
    """
    def __init__(self, bus):
        super().__init__(bus, name="gold_scanner")
        self.evaluator = DealEvaluator()
        # Имитация живой котировки: цена за 1г чистого золота 999
        self.gold_spot_price_usd = 77.50 

    def fetch_items(self):
        # Реальный кейс: цена ниже стоимости металла — это 10/10 сделка
        return [
            {
                "id": "gold-ring-585",
                "title": "Кольцо мужское, 585 проба",
                "weight": 12.0,
                "purity": 0.585,
                "price": 450.0,      # Цена продавца
                "market_item_price": 700.0, # Цена как изделия в магазине
                "nuances": ["Потертости", "Нужна полировка", "Нет пробы (нужна проверка)"]
            }
        ]

    def run_scan(self):
        for raw in self.fetch_items():
            # Расчет стоимости чистого веса металла (цена лома)
            melt_value = raw["weight"] * raw["purity"] * self.gold_spot_price_usd
            
            # Анализ через ядро DonMir
            # Расходы: 20$ на проверку и полировку
            res = self.evaluator.analyze(
                price=raw["price"], 
                market_price=melt_value, # Берем за базу цену лома (самая безопасная оценка)
                overheads=20.0, 
                min_profit=100.0, 
                nuances=raw["nuances"]
            )

            report = (
                f"\n--- 💍 ЗОЛОТОЙ АРБИТРАЖ DonMir ---\n"
                f"Объект: {raw['title']}\n"
                f"Вес: {raw['weight']}г | Чистый металл: {melt_value:.1f}$\n"
                f"Зона: {res['zone']}\n"
                f"РЕКОМЕНДАЦИЯ: {res['advice']}\n"
                f"--- АРГУМЕНТЫ ДЛЯ ТОРГА ---\n"
                + "\n".join(res['scripts'])
            )
            
            logger.info(report)
            self.process_and_publish(ListingItem(id=raw["id"], title=raw["title"], price=raw["price"], url=""))
