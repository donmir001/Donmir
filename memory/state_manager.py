import json
import logging
from pathlib import Path
from typing import Any, Dict


class StateManager:
    """Менеджер сохранения и загрузки состояния агента на диск."""

    def __init__(self, storage_path: str = "memory/state.json"):
        self.storage_path = Path(storage_path)
        self._state: Dict[str, Any] = {}
        self.load_state()

    def load_state(self) -> Dict[str, Any]:
        """Загружает состояние из файла JSON, если он существует."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self._state = json.load(f)
            except Exception as e:
                logging.error(f"Ошибка загрузки состояния из {self.storage_path}: {e}")
                self._state = {}
        return self._state

    def save_state(self) -> None:
        """Записывает текущее состояние в файл JSON."""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self._state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Ошибка сохранения состояния в {self.storage_path}: {e}")

    def set(self, key: str, value: Any) -> None:
        """Записывает ключ-значение и автоматически сохраняет на диск."""
        self._state[key] = value
        self.save_state()

    def get(self, key: str, default: Any = None) -> Any:
        """Возвращает значение по ключу из памяти."""
        return self._state.get(key, default)

    def clear(self) -> None:
        """Очищает память и файл состояния."""
        self._state.clear()
        self.save_state()
