from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError
from fastapi import status

class OrderNotFoundError(FoodDeliveryDomainError):
    def __init__(self, order_id: str) -> None:
        super().__init__(code="order_not_found", status_code=status.HTTP_404_NOT_FOUND)
        self.order_id = order_id
