from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, order_id: str) -> Optional[Order]:
        raise NotImplementedError

    @abstractmethod
    def list_for_customer(self, customer_id: str) -> List[Order]:
        raise NotImplementedError
