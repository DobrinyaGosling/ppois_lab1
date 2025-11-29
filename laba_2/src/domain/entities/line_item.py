from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from src.domain.value_objects.money import Money


@dataclass
class LineItem:
    item_id: str
    name: str
    quantity: int
    unit_price: Money

    def total(self) -> Money:
        return self.unit_price.multiply(Decimal(self.quantity))
