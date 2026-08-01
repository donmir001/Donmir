import json
import logging
from pathlib import Path
from typing import Any, Dict, List


class SessionStore:
    """Хранилище истории событий и сообщений по сессиям агента."""

    def __init__(self, sessions_dir: str = "memory/sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_path(self, session_id: str) -> Path:
        return self.sessions_dir / f"{session_id}.json"

    def add_event(self, session_id: str, event_type: str, payload: Any = None) -> None:
        """Записывает новое событие в историю сессии."""
        session_file = self._get_session_path(session_id)
        history = self.get_session_history(session_id)

        history.append({"event": event_type, "payload": payload})

        try:
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Ошибка записи истории сессии '{session_id}': {e}")

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Возвращает полную историю событий для указанной сессии."""
        session_file = self._get_session_path(session_id)
        if not session_file.exists():
            return []

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Ошибка чтения истории сессии '{session_id}': {e}")
            return []
