from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class InsufficientFundsError(FoodDeliveryDomainError):
    def __init__(self, card_id: str) -> None:
        super().__init__(code="insufficient_funds")
        self.card_id = card_id
