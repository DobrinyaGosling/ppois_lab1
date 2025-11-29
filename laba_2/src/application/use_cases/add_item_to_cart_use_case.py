from __future__ import annotations

from dataclasses import dataclass

from src.application.repositories import CartRepository, RestaurantRepository
from src.domain.entities.line_item import LineItem
from src.exceptions import MenuItemNotAvailableError, RestaurantClosedError


@dataclass
class AddItemToCartUseCase:
    cart_repository: CartRepository
    restaurant_repository: RestaurantRepository

    def execute(self, customer_id: str, restaurant_id: str, item_id: str, quantity: int):
        cart = self.cart_repository.get_cart(customer_id)
        restaurant = self.restaurant_repository.get(restaurant_id)
        if not restaurant:
            raise RestaurantClosedError(restaurant_id)
        menu_item = restaurant.get_menu_item(item_id)
        if not menu_item:
            raise MenuItemNotAvailableError(item_id)
        cart.add_item(LineItem(item_id=item_id, name=menu_item.name, quantity=quantity, unit_price=menu_item.price))
        self.cart_repository.save_cart(cart)
        return cart
