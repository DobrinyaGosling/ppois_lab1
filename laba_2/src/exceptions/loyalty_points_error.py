from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class LoyaltyPointsError(FoodDeliveryDomainError):
    def __init__(self, customer_id: str) -> None:
        super().__init__(code="loyalty_error")
        self.customer_id = customer_id
