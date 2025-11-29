from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class CartEmptyError(FoodDeliveryDomainError):
    def __init__(self, cart_id: str) -> None:
        super().__init__(code="cart_empty")
        self.cart_id = cart_id
