from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.entities.cart import Cart


class CartRepository(ABC):
    @abstractmethod
    def get_cart(self, customer_id: str) -> Cart:
        raise NotImplementedError

    @abstractmethod
    def save_cart(self, cart: Cart) -> None:
        raise NotImplementedError
