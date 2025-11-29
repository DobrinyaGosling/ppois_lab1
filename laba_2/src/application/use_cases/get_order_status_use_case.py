from __future__ import annotations

from dataclasses import dataclass

from src.application.repositories import OrderRepository
from src.exceptions import OrderNotFoundError


@dataclass
class GetOrderStatusUseCase:
    order_repository: OrderRepository

    def execute(self, order_id: str) -> str:
        order = self.order_repository.get(order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        return order.status
