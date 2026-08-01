from memory.state_manager import StateManager


def test_state_manager_set_and_get(tmp_path):
    """Тест сохранения и чтение данных из памяти."""
    state_file = tmp_path / "state.json"
    sm = StateManager(str(state_file))

    sm.set("session_id", "session_999")
    assert sm.get("session_id") == "session_999"

    # Проверяем персистентность (восстановление из файла новым экземпляром)
    sm_reloaded = StateManager(str(state_file))
    assert sm_reloaded.get("session_id") == "session_999"


def test_state_manager_clear(tmp_path):
    """Тест очистки состояния."""
    state_file = tmp_path / "state.json"
    sm = StateManager(str(state_file))

    sm.set("temp_key", "temp_val")
    sm.clear()

    assert sm.get("temp_key") is None
