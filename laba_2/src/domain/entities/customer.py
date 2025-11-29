from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.domain.entities.payment_card import PaymentCard
from src.domain.value_objects.address import Address


@dataclass
class Customer:
    customer_id: str
    name: str
    address: Address
    hashed_password: str
    salt: str
    loyalty_points: int
    cards: List[PaymentCard]

    def add_points(self, points: int) -> None:
        self.loyalty_points += max(points, 0)

    def redeem_points(self, points: int) -> None:
        if points > self.loyalty_points:
            raise ValueError("Not enough loyalty points")
        self.loyalty_points -= points

    def primary_card(self) -> Optional[PaymentCard]:
        return self.cards[0] if self.cards else None
