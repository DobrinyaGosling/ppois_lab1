from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class CourierUnavailableError(FoodDeliveryDomainError):
    def __init__(self, zone: str) -> None:
        super().__init__(code="courier_unavailable")
        self.zone = zone
