from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class PromoCodeExpiredError(FoodDeliveryDomainError):
    def __init__(self, code_value: str) -> None:
        super().__init__(code="promo_code_invalid")
        self.code_value = code_value
