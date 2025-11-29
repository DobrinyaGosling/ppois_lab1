from src.exceptions.food_delivery_domain_error import FoodDeliveryDomainError


class MenuItemNotAvailableError(FoodDeliveryDomainError):
    def __init__(self, item_id: str) -> None:
        super().__init__(code="menu_item_unavailable")
        self.item_id = item_id
