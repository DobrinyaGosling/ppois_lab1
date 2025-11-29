from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class PaymentFailedError(FoodDeliveryDomainError):
    def __init__(self, reason: str) -> None:
        super().__init__(code="payment_failed")
        self.reason = reason
