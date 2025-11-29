from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.menu_item import MenuItem
from src.domain.entities.restaurant import Restaurant


class RestaurantRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Restaurant]:
        raise NotImplementedError

    @abstractmethod
    def get(self, restaurant_id: str) -> Optional[Restaurant]:
        raise NotImplementedError

    @abstractmethod
    def list_menu(self, restaurant_id: str) -> List[MenuItem]:
        raise NotImplementedError
