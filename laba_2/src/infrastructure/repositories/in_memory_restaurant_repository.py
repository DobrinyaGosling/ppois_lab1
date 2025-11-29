from __future__ import annotations

from decimal import Decimal
from typing import Dict, List, Optional

from src.application.repositories import RestaurantRepository
from src.domain.entities.menu_item import MenuItem
from src.domain.entities.restaurant import Restaurant
from src.domain.value_objects.address import Address
from src.domain.value_objects.money import Money


class InMemoryRestaurantRepository(RestaurantRepository):
    def __init__(self) -> None:
        margherita = MenuItem("m1", "Margherita", Money(Decimal("12.00"), "USD"))
        pepperoni = MenuItem("m2", "Pepperoni", Money(Decimal("14.00"), "USD"))
        sushi = MenuItem("s1", "Sushi Set", Money(Decimal("18.00"), "USD"))
        ramen = MenuItem("s2", "Ramen", Money(Decimal("15.00"), "USD"))
        self.restaurants: Dict[str, Restaurant] = {
            "r1": Restaurant("r1", "Pasta Plaza", Address("Main", "Minsk", "central"), [margherita, pepperoni], 9, 23),
            "r2": Restaurant("r2", "Sushi Spot", Address("Side", "Minsk", "north"), [sushi, ramen], 10, 22),
        }

    def list_all(self) -> List[Restaurant]:
        return list(self.restaurants.values())

    def get(self, restaurant_id: str) -> Optional[Restaurant]:
        return self.restaurants.get(restaurant_id)

    def list_menu(self, restaurant_id: str) -> List[MenuItem]:
        restaurant = self.restaurants.get(restaurant_id)
        return restaurant.menu if restaurant else []
