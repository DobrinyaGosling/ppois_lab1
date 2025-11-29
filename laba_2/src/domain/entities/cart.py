from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from src.domain.entities.line_item import LineItem
from src.domain.value_objects.money import Money


@dataclass
class Cart:
    cart_id: str
    customer_id: str
    items: List[LineItem] = field(default_factory=list)
    promo_code: Optional[str] = None

    def add_item(self, item: LineItem) -> None:
        for existing in self.items:
            if existing.item_id == item.item_id:
                existing.quantity += item.quantity
                return
        self.items.append(item)

    def total(self) -> Money:
        total = Money(Decimal("0.00"), "USD")
        for item in self.items:
            total = total.add(item.total())
        return total
