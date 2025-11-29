
from typing import Dict, List

from src.application.repositories.reservation_repository import ReservationRepository
from src.domain.entities.reservation import ReservationRecord


class InMemoryReservationRepository(ReservationRepository):

    def __init__(self) -> None:
        self.reservation_storage_map: Dict[str, ReservationRecord] = {}

    def save_reservation(self, reservation: ReservationRecord) -> None:
        self.reservation_storage_map[reservation.reservation_id] = reservation

    def list_reservations_for_customer(self, customer_id: str) -> List[ReservationRecord]:
        return [res for res in self.reservation_storage_map.values() if res.reservation_customer_id == customer_id]

    def get_reservation(self, reservation_id: str) -> ReservationRecord | None:
        return self.reservation_storage_map.get(reservation_id)
