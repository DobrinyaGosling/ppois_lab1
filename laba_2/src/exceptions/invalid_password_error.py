from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class InvalidPasswordError(FoodDeliveryDomainError):
    def __init__(self, customer_id: str) -> None:
        super().__init__(code="invalid_password")
        self.customer_id = customer_id
