from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.courier import Courier


class CourierRepository(ABC):
    @abstractmethod
    def list_available(self, zone: str) -> List[Courier]:
        raise NotImplementedError

    @abstractmethod
    def save(self, courier: Courier) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, courier_id: str) -> Optional[Courier]:
        raise NotImplementedError
