from __future__ import annotations

from typing import Dict, List, Optional

from src.application.repositories import OrderRepository
from src.domain.entities.order import Order


class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self.orders: Dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[order.order_id] = order

    def get(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)

    def list_for_customer(self, customer_id: str) -> List[Order]:
        return [order for order in self.orders.values() if order.customer_id == customer_id]
