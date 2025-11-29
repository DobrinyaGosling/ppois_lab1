from __future__ import annotations

from typing import Dict

from src.application.repositories import CartRepository
from src.domain.entities.cart import Cart


class InMemoryCartRepository(CartRepository):
    def __init__(self) -> None:
        self.carts: Dict[str, Cart] = {}

    def get_cart(self, customer_id: str) -> Cart:
        return self.carts.setdefault(customer_id, Cart(cart_id=f"cart-{customer_id}", customer_id=customer_id))

    def save_cart(self, cart: Cart) -> None:
        self.carts[cart.customer_id] = cart
