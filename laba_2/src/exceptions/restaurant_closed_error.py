from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class RestaurantClosedError(FoodDeliveryDomainError):
    def __init__(self, restaurant_id: str) -> None:
        super().__init__(code="restaurant_closed")
        self.restaurant_id = restaurant_id
