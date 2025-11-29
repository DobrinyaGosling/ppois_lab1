from __future__ import annotations

from dataclasses import dataclass

from src.application.repositories import CartRepository, PromoCodeRepository, RestaurantRepository
from src.exceptions import PromoCodeExpiredError, RestaurantClosedError


@dataclass
class ApplyPromoUseCase:
    cart_repository: CartRepository
    promo_repository: PromoCodeRepository
    restaurant_repository: RestaurantRepository

    def execute(self, customer_id: str, promo_code: str, restaurant_id: str):
        cart = self.cart_repository.get_cart(customer_id)
        restaurant = self.restaurant_repository.get(restaurant_id)
        if not restaurant:
            raise RestaurantClosedError(restaurant_id)
        promo = self.promo_repository.get(promo_code)
        if not promo or not promo.applicable(cart.total(), restaurant_id):
            raise PromoCodeExpiredError(promo_code)
        cart.promo_code = promo_code
        self.cart_repository.save_cart(cart)
        return cart
