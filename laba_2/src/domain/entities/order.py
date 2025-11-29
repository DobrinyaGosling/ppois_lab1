from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.domain.entities.line_item import LineItem
from src.domain.value_objects.address import Address
from src.domain.value_objects.money import Money


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[LineItem]
    total_amount: Money
    status: str
    delivery_address: Address
    courier_id: Optional[str]

    def update_status(self, new_status: str) -> None:
        self.status = new_status

    def assign_courier(self, courier_id: str) -> None:
        self.courier_id = courier_id
