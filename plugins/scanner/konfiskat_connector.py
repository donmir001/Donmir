import logging
from plugins.scanner.base_scanner import BaseScanner, ListingItem
from core.evaluator import DealEvaluator

logger = logging.getLogger("DonMir.Konfiskat")

class KonfiskatConnector(BaseScanner):
    """
    Гениальный коннектор госаукционов.
    Рассчитывает математическое ожидание победы и точку выхода.
    """
    def __init__(self, bus):
        super().__init__(bus, name="konfiskat_connector")
        self.evaluator = DealEvaluator()
        self.auction_step_pct = 0.05 # Шаг аукциона 5%

    def fetch_items(self):
        # Кейс: Лот на ТД Восточный
        return [{
            "id": "lot-vost-2026",
            "title": "Складской остаток: Набор инструментов Makita (100 шт)",
            "start_price": 2000.0,
            "market_value": 5500.0,
            "overheads": 150.0, # Хранение и вывоз
            "nuances": ["Упаковка повреждена", "Нет гарантии", "Партия неделимая"]
        }]

    def run_scan(self):
        for raw in self.fetch_items():
            # ГЛУБОКАЯ АНАЛИТИКА
            res = self.evaluator.analyze(
                price=raw["start_price"],
                market_price=raw["market_value"],
                overheads=raw["overheads"],
                min_profit=1500.0, # На опте хотим больше
                nuances=raw["nuances"]
            )
            
            # РАСЧЕТ АУКЦИОННОЙ СТРАТЕГИИ (ГЕНИАЛЬНОСТЬ)
            max_allowed_bid = res["max_bid"]
            recommended_steps = int((max_allowed_bid - raw["start_price"]) / (raw["start_price"] * self.auction_step_pct))

            report = (
                f"\n--- ⚖️ СУДЕБНЫЙ АРБИТРАЖ DonMir ---\n"
                f"ЛОТ: {raw['title']}\n"
                f"РЫНОК: {raw['market_value']}$ | СТАРТ: {raw['start_price']}$\n"
                f"Зона: {res['zone']}\n"
                f"ЦЕЛЬ ТОРГОВ: Не выше {max_allowed_bid:.0f}$ (Запас: {recommended_steps} шагов)\n"
                f"ОБОСНОВАНИЕ ДЛЯ ПЕРЕПРОДАЖИ:\n" + "\n".join(res['scripts'])
            )
            
            logger.info(report)
            self.process_and_publish(ListingItem(id=raw["id"], title=raw["title"], price=raw["start_price"], url=""))
