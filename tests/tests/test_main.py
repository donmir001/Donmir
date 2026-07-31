from main import (
    APP_NAME,
    DEFAULT_CONFIG,
    get_boot_message,
    get_system_info,
    load_config,
)


def test_boot_message_content():
    """Проверка приветственного сообщения с конфигом."""
    message = get_boot_message(DEFAULT_CONFIG)
    assert APP_NAME in message
    assert "Version 0.1" in message
    assert "System initialized." in message


def test_system_info_content():
    """Проверка вывода системных данных с конфигом."""
    info = get_system_info(DEFAULT_CONFIG)
    assert "Platform started" in info
    assert "Project: DonMir" in info
    assert "Mode: development" in info
    assert "Data Path: ./storage" in info
    assert "Status: Ready" in info


def test_config_fallback_when_missing(tmp_path):
    """Тест безопасного отката на дефолтный конфиг при отсутствии файла."""
    missing_file = tmp_path / "non_existent.json"
    config = load_config(missing_file)
    assert config == DEFAULT_CONFIG
