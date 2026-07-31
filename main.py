
VERSION = "0.1"
APP_NAME = "DonMir Boot Agent"


def get_boot_message() -> str:
    """Формирует стартовое сообщение Boot Agent."""
    return f"{APP_NAME}\n\nVersion {VERSION}\n\nSystem initialized."


def main() -> None:
    """Точка входа в приложение."""
    print(get_boot_message())


if __name__ == "__main__":
    main()
