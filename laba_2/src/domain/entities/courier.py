from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Courier:
    courier_id: str
    name: str
    home_zone: str
    active: bool
    current_order_id: Optional[str] = None

    def is_available(self) -> bool:
        return self.active and self.current_order_id is None

    def assign_order(self, order_id: str) -> None:
        self.current_order_id = order_id

    def complete_order(self) -> None:
        self.current_order_id = None
