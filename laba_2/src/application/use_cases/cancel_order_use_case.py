from __future__ import annotations

from dataclasses import dataclass

from src.application.repositories import CourierRepository, OrderRepository
from src.exceptions import OrderAlreadyDeliveredError, OrderNotFoundError


@dataclass
class CancelOrderUseCase:
    order_repository: OrderRepository
    courier_repository: CourierRepository

    def execute(self, order_id: str):
        order = self.order_repository.get(order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        if order.status == "delivered":
            raise OrderAlreadyDeliveredError(order_id)
        order.update_status("cancelled")
        if order.courier_id:
            courier = self.courier_repository.get(order.courier_id)
            if courier:
                courier.complete_order()
                self.courier_repository.save(courier)
        self.order_repository.save(order)
        return order
