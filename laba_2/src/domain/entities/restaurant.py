from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.domain.entities.menu_item import MenuItem
from src.domain.value_objects.address import Address


@dataclass
class Restaurant:
    restaurant_id: str
    name: str
    address: Address
    menu: List[MenuItem]
    open_hour: int
    close_hour: int

    def is_open_at(self, hour: int) -> bool:
        return self.open_hour <= hour < self.close_hour

    def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        return next((item for item in self.menu if item.item_id == item_id and item.available), None)
