from main import (
    APP_NAME,
    DEFAULT_CONFIG,
    get_boot_message,
    get_system_info,
    load_config,
    log_boot_event,
)


def test_boot_message_content():
    message = get_boot_message(DEFAULT_CONFIG)
    assert APP_NAME in message
    assert "Version 0.1" in message
    assert "System initialized." in message


def test_system_info_content():
    info = get_system_info(DEFAULT_CONFIG)
    assert "Platform started" in info
    assert "Project: DonMir" in info
    assert "Mode: development" in info
    assert "Data Path: ./storage" in info
    assert "Status: Ready" in info


def test_config_fallback_when_missing(tmp_path):
    missing_file = tmp_path / "non_existent.json"
    config = load_config(missing_file)
    assert config == DEFAULT_CONFIG


def test_log_boot_event(tmp_path):
    """Тест записи события запуска в лог-файл."""
    test_log = tmp_path / "boot.log"
    entry = log_boot_event(
        DEFAULT_CONFIG, status="INITIALIZED", log_file=test_log
    )

    assert test_log.exists()
    assert "Version: 0.1" in entry
    assert "Status: INITIALIZED" in entry

    content = test_log.read_text()
    assert entry in content
