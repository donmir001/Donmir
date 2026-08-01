import logging
from pathlib import Path
from core.config_manager import ConfigManager
from core.system import SystemCore


def setup_logging():
    """Настройка логирования работы агента."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=log_dir / "boot.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )


def main():
    setup_logging()
    logging.info("Инициализация DonMir Boot Agent...")

    # Работа с ядром платформы
    config_mgr = ConfigManager()
    sys_core = SystemCore(config_mgr)

    sys_core.initialize()
    info = sys_core.get_system_info()

    welcome_msg = (
        f"Привет! Я {info['agent_name']} v{info['version']} "
        f"на базе {info['os']} {info['os_release']} (Python {info['python_version']})"
    )

    print(welcome_msg)
    logging.info(f"Успешный запуск ядра: {welcome_msg}")

    sys_core.shutdown()


if __name__ == "__main__":
    main()
