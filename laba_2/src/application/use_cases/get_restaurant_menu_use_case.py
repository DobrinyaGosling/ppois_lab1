from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.application.repositories import RestaurantRepository
from src.domain.entities.menu_item import MenuItem
from src.exceptions import RestaurantClosedError


@dataclass
class GetRestaurantMenuUseCase:
    restaurant_repository: RestaurantRepository

    def execute(self, restaurant_id: str) -> List[MenuItem]:
        restaurant = self.restaurant_repository.get(restaurant_id)
        if not restaurant:
            raise RestaurantClosedError(restaurant_id)
        return [item for item in restaurant.menu if item.available]
