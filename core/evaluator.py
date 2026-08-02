from typing import Dict, Any, List

class DealEvaluator:
    """Центральный интеллект DonMir для оценки маржинальности и рисков."""

    @staticmethod
    def analyze(price: float, market_price: float, overheads: float, min_profit: float, nuances: List[str]) -> Dict[str, Any]:
        # Расчет финансового скелета
        break_even = market_price - overheads
        target_buy_price = market_price - overheads - min_profit

        if price <= target_buy_price:
            zone, advice = "🟢 ЗЕЛЕНАЯ", "Забирай немедленно. Цена ниже целевой!"
        elif price < break_even:
            zone, advice = "🟡 ЖЕЛТАЯ", f"Нужен торг. Сбивай до {target_buy_price:.0f}$"
        else:
            zone, advice = "🔴 КРАСНАЯ", "Пропускай. Сделка принесет убыток."

        scripts = [f"• {n} (использовать для снижения цены)" for n in nuances]
        
        return {
            "zone": zone,
            "target_price": target_buy_price,
            "max_bid": break_even,
            "advice": advice,
            "scripts": scripts
        }
