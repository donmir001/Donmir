from typing import Dict, Any, List, Optional
from plugins.scanner.base_scanner import BaseScanner, ListingItem

class GoldScanner(BaseScanner):
    """Сканер драгметаллов."""

    def __init__(self, bus):
        super().__init__(bus, name="gold_scanner")

    def fetch_items(self) -> List[Dict[str, Any]]:
        return []

    def parse_item(self, raw_item: Dict[str, Any]) -> Optional[ListingItem]:
        # Это тот самый метод, которого не хватало
        return None

    def run_scan(self) -> List[ListingItem]:
        return []
