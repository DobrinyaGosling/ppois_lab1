from __future__ import annotations

from typing import Dict, List, Optional

from src.application.repositories import CourierRepository
from src.domain.entities.courier import Courier


class InMemoryCourierRepository(CourierRepository):
    def __init__(self) -> None:
        self.couriers: Dict[str, Courier] = {
            "c1": Courier("c1", "Alex", "central", True),
            "c2": Courier("c2", "Ira", "north", True),
        }

    def list_available(self, zone: str) -> List[Courier]:
        return [courier for courier in self.couriers.values() if courier.home_zone == zone and courier.is_available()]

    def save(self, courier: Courier) -> None:
        self.couriers[courier.courier_id] = courier

    def get(self, courier_id: str) -> Optional[Courier]:
        return self.couriers.get(courier_id)
