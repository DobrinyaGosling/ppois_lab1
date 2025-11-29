
from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.reservation import ReservationRecord


class ReservationRepository(ABC):

    @abstractmethod
    def save_reservation(self, reservation: ReservationRecord) -> None: ...

    @abstractmethod
    def list_reservations_for_customer(self, customer_id: str) -> List[ReservationRecord]: ...

    @abstractmethod
    def get_reservation(self, reservation_id: str) -> ReservationRecord | None: ...
