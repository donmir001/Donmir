from plugins.scanner.base_scanner import BaseScanner

class KonfiskatConnector(BaseScanner):
    """Коннектор для мониторинга аукционов и конфиската."""

    def __init__(self, bus):
        super().__init__(bus, name="konfiskat_connector")

    def fetch_items(self):
        # Заглушка для будущей интеграции с ТД Восточный
        return []

    def run_scan(self):
        return []
