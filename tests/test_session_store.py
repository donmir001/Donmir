from memory.session_store import SessionStore


def test_session_store_add_and_get(tmp_path):
    """Тест сохранения и чтения истории сессии."""
    store = SessionStore(str(tmp_path))

    store.add_event("session_001", "user_prompt", "Привет, агент!")
    store.add_event("session_001", "agent_reply", "Привет! Чем могу помочь?")

    history = store.get_session_history("session_001")
    assert len(history) == 2
    assert history[0]["event"] == "user_prompt"
    assert history[0]["payload"] == "Привет, агент!"
    assert history[1]["event"] == "agent_reply"


def test_session_store_non_existent_session(tmp_path):
    """Тест запроса истории несуществующей сессии."""
    store = SessionStore(str(tmp_path))
    assert store.get_session_history("unknown_session") == []
