import logging
from typing import Any, Callable, Dict, List


class EventBus:
    """Базовая шина событий для слабой связанности компонентов платформы."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """Подписка функции-обработчика на событие."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """Отписка функции-обработчика от события."""
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)

    def publish(self, event_type: str, data: Any = None) -> None:
        """Публикация события и вызов всех подписчиков."""
        if event_type in self._subscribers:
            for callback in list(self._subscribers[event_type]):
                try:
                    callback(data)
                except Exception as e:
                    logging.error(f"Ошибка при обработке события '{event_type}': {e}")
