from __future__ import annotations

from dataclasses import dataclass

from src.application.repositories import CartRepository
from src.domain.value_objects.money import Money


@dataclass
class SummarizeCartUseCase:
    cart_repository: CartRepository

    def execute(self, customer_id: str) -> Money:
        cart = self.cart_repository.get_cart(customer_id)
        return cart.total()
