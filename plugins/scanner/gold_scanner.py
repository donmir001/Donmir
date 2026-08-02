from typing import Dict, Any, List, Optional
from core.event_bus import EventBus
from plugins.scanner.base_scanner import BaseScanner, ListingItem

class GoldScanner(BaseScanner):
    """Сканер золота и драгметаллов."""
    def __init__(self, bus: EventBus):
        super().__init__(bus, name="gold_scanner")

    def fetch_items(self) -> List[Dict[str, Any]]:
        return [] # Пока пусто

    def run_scan(self) -> List[ListingItem]:
        return []
