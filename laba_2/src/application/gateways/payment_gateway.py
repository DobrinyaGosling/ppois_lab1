from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.entities.customer import Customer
from src.domain.entities.order import Order


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, customer: Customer, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    def apply_loyalty(self, customer: Customer, amount: int) -> None:
        raise NotImplementedError
