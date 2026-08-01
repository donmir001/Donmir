import logging
from pathlib import Path
from core.config_manager import ConfigManager
from core.event_bus import EventBus
from core.plugin_manager import PluginManager
from core.system import SystemCore
from executor.task_runner import TaskRunner
from memory.session_store import SessionStore
from memory.state_manager import StateManager


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
    logging.info("Инициализация полной платформы DonMir Boot Agent...")

    # 1. Инициализация Шины Событий и Ядра
    event_bus = EventBus()
    config_mgr = ConfigManager()
    sys_core = SystemCore(config_mgr, event_bus)

    # 2. Инициализация подсистем Памяти, Плагинов и Исполнителя
    state_mgr = StateManager()
    session_store = SessionStore()
    plugin_mgr = PluginManager()
    task_runner = TaskRunner(event_bus)

    # 3. Запуск ядра
    sys_core.initialize()
    info = sys_core.get_system_info()

    # 4. Сканирование плагинов
    plugins = plugin_mgr.discover_plugins()
    state_mgr.set("discovered_plugins", plugins)

    # 5. Регистрация и запуск тестовой задачи
    task_runner.register_task("ping", lambda: "pong")
    result = task_runner.run_task("ping")

    session_store.add_event("system_boot", "boot_completed", {"ping_result": result})

    welcome_msg = (
        f"Привет! Я {info['agent_name']} v{info['version']} "
        f"на базе {info['os']} {info['os_release']} (Python {info['python_version']}). "
        f"Платформа полностью активна!"
    )

    print(welcome_msg)
    logging.info(welcome_msg)

    # 6. Остановка ядра
    sys_core.shutdown()


if __name__ == "__main__":
    main()
