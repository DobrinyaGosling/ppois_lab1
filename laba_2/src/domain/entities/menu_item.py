from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from src.domain.value_objects.money import Money


@dataclass
class MenuItem:
    item_id: str
    name: str
    price: Money
    available: bool = True

    def mark_unavailable(self) -> None:
        self.available = False

    def adjust_price(self, delta: Decimal) -> None:
        self.price = self.price.add(Money(delta, self.price.currency))
