import logging
from typing import Any, Callable, Dict
from core.event_bus import EventBus


class TaskRunner:
    """Движок выполнения и оркестрации задач агента."""

    def __init__(self, event_bus: EventBus = None):
        self.event_bus = event_bus or EventBus()
        self._tasks: Dict[str, Callable[..., Any]] = {}

    def register_task(self, name: str, func: Callable[..., Any]) -> None:
        """Регистрирует именованную задачу в исполнителе."""
        self._tasks[name] = func
        logging.info(f"Задача '{name}' успешно зарегистрирована.")

    def run_task(self, name: str, *args, **kwargs) -> Any:
        """Запускает задачу по имени и генерирует события."""
        if name not in self._tasks:
            error_msg = f"Задача '{name}' не найдена в реестре."
            logging.error(error_msg)
            self.event_bus.publish("task_failed", {"task_name": name, "error": error_msg})
            raise KeyError(error_msg)

        self.event_bus.publish("task_started", {"task_name": name})
        try:
            result = self._tasks[name](*args, **kwargs)
            self.event_bus.publish("task_completed", {"task_name": name, "result": result})
            return result
        except Exception as e:
            logging.error(f"Ошибка при выполнении задачи '{name}': {e}")
            self.event_bus.publish("task_failed", {"task_name": name, "error": str(e)})
            raise e
