from typing import List, Dict, Any

class PersuasionEngine:
    """
    Движок Когнитивного Превосходства DonMir.
    Синтез техник КГБ (рефлексивное управление), Моссад (таргетирование) и ФБР.
    """

    @staticmethod
    def get_strategy(category: str, artifacts: List[str], profile: Dict[str, Any]) -> Dict[str, Any]:
        tactics = []
        
        # 1. Техника КГБ: 'Рефлексивное управление' (Reflexive Control)
        # Суть: передать продавцу информацию так, чтобы он сам захотел снизить цену.
        if artifacts:
            tactics.append({
                "source": "KGB Operational Psych",
                "method": "The Inevitable Depreciation",
                "action": "Создайте у продавца страх 'завтрашнего падения цены'.",
                "phrase": "Я вижу износ педалей и руля. Через месяц этот дефект станет критическим, и машина 'зависнет'. Я — ваш шанс выйти из актива с деньгами сегодня."
            })

        # 2. Техника Mossad: 'Targeted Pressure' (Точечное давление)
        if profile.get("urgency"):
            tactics.append({
                "source": "Mossad Efficiency",
                "method": "The Single Exit",
                "action": "Демонстрация отсутствия альтернатив у продавца.",
                "phrase": "Рынок перенасыщен такими iPhone с изношенным АКБ. Мое предложение — единственное 'живое' на этой неделе. Сделка сейчас или никогда."
            })

        # 3. Техника MI6: 'High-Level Authority' (Легендирование)
        tactics.append({
            "source": "MI6 Social Engineering",
            "method": "The Expert Disappointment",
            "action": "Тон вежливого, но крайне разочарованного профессионала.",
            "phrase": "Жаль. Я рассчитывал на коллекционное состояние, но вижу следы небрежного использования. Это меняет категорию товара на 'утилитарный лом'."
        })

        return {
            "tactics": tactics,
            "operational_tone": "Холодный, аналитический, доминирующий через спокойствие."
        }
