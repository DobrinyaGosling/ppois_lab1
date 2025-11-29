from __future__ import annotations

from dataclasses import dataclass

from src.domain.value_objects.money import Money


@dataclass
class PaymentCard:
    card_id: str
    masked_number: str
    balance: Money
    active: bool = True

    def charge(self, amount: Money) -> None:
        if not self.active:
            raise ValueError("Card inactive")
        if self.balance.amount < amount.amount:
            raise ValueError("Insufficient card balance")
        self.balance = self.balance.subtract(amount)

    def credit(self, amount: Money) -> None:
        self.balance = self.balance.add(amount)
