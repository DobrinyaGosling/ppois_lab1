from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from src.domain.value_objects.money import Money


@dataclass
class PromoCode:
    code: str
    discount_percent: int
    restaurant_id: Optional[str]
    min_order_amount: Money
    uses_left: int

    def applicable(self, total: Money, restaurant_id: str) -> bool:
        if self.restaurant_id and self.restaurant_id != restaurant_id:
            return False
        if total.amount < self.min_order_amount.amount:
            return False
        return self.uses_left > 0

    def apply(self, total: Money) -> Money:
        discount = total.multiply(Decimal(self.discount_percent) / Decimal(100))
        self.uses_left -= 1
        return total.subtract(discount)
