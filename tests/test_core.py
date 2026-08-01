import json
import pytest
from core.config_manager import ConfigManager
from core.system import SystemCore


def test_config_manager_load_success(tmp_path):
    """Тест успешной загрузки конфигурации."""
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps({"agent_name": "TestAgent", "version": "1.0.0"}), encoding="utf-8")

    config_mgr = ConfigManager(str(cfg_file))
    data = config_mgr.load_config()

    assert data["agent_name"] == "TestAgent"
    assert config_mgr.get("agent_name") == "TestAgent"
    assert config_mgr.get("non_existent", "default") == "default"


def test_config_manager_file_not_found():
    """Тест обработки отсутствия файла конфигурации."""
    config_mgr = ConfigManager("non_existent_path.json")
    with pytest.raises(FileNotFoundError):
        config_mgr.load_config()


def test_system_core_lifecycle(tmp_path):
    """Тест цикла жизни SystemCore и получения информации."""
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps({"agent_name": "CoreAgent", "version": "2.0.0"}), encoding="utf-8")

    config_mgr = ConfigManager(str(cfg_file))
    sys_core = SystemCore(config_mgr)

    assert not sys_core.is_running
    sys_core.initialize()
    assert sys_core.is_running

    info = sys_core.get_system_info()
    assert info["agent_name"] == "CoreAgent"
    assert info["version"] == "2.0.0"
    assert "os" in info

    sys_core.shutdown()
    assert not sys_core.is_running
