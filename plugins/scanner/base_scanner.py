from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from core.event_bus import EventBus


@dataclass
class ListingItem:
    """Стандартизированная модель найденного объявления."""
    id: str
    title: str
    price: float
    estimated_market_price: float
    url: str
    category: str
    raw_data: Optional[Dict[str, Any]] = None

    @property
    def profit_margin(self) -> float:
        """Расчет маржинальности в процентах."""
        if self.estimated_market_price <= 0:
            return 0.0
        return ((self.estimated_market_price - self.price) / self.estimated_market_price) * 100


class BaseScanner(ABC):
    """Базовый класс для всех сканеров экосистемы DonMir."""

    def __init__(self, bus: EventBus, name: str = "base_scanner"):
        self.bus = bus
        self.name = name

    @abstractmethod
    def fetch_items(self) -> List[Dict[str, Any]]:
        """Получение сырых данных объявлений."""
        pass

    @abstractmethod
    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        """Парсинг сырого объявления в ListingItem."""
        pass

    def process_and_publish(self, item: ListingItem) -> None:
        """Анализ выгоды и публикация событий в EventBus."""
        # Публикуем событие об обработанном товаре
        self.bus.publish("scanner:item_found", item.__dict__)

        # Если выгода 15% и более — генерируем событие сделки
        if item.profit_margin >= 15.0:
            self.bus.publish("scanner:deal_detected", item.__dict__)
