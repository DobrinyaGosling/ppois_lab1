from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.application.repositories import RestaurantRepository
from src.domain.entities.restaurant import Restaurant


@dataclass
class ListRestaurantsUseCase:
    restaurant_repository: RestaurantRepository

    def execute(self) -> List[Restaurant]:
        return self.restaurant_repository.list_all()
