VERSION = "0.1"
APP_NAME = "DonMir Boot Agent"
PROJECT_NAME = "DonMir"
STATUS = "Ready"


def get_boot_message() -> str:
    """Формирует стартовое сообщение Boot Agent."""
    return f"{APP_NAME}\n\nVersion {VERSION}\n\nSystem initialized."


def get_system_info() -> str:
    """Формирует информацию о состоянии платформы."""
    return f"Platform started\nProject: {PROJECT_NAME}\nStatus: {STATUS}"


def main() -> None:
    """Точка входа в приложение."""
    print(get_boot_message())
    print()
    print(get_system_info())


if __name__ == "__main__":
    main()
