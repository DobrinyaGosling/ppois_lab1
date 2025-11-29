
from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError
from fastapi import status


class CustomerNotFoundError(FoodDeliveryDomainError):
    def __init__(self, customer_id: str) -> None:
        super().__init__(code="customer_not_found", status_code=status.HTTP_404_NOT_FOUND)
        self.customer_id = customer_id
