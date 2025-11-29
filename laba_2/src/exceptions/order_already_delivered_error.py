from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class OrderAlreadyDeliveredError(FoodDeliveryDomainError):
    def __init__(self, order_id: str) -> None:
        super().__init__(code="order_delivered")
        self.order_id = order_id
