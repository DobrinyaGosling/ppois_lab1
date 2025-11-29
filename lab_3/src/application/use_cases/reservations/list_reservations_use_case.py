"""Use case for listing reservations."""

from typing import List

from src.application.repositories.reservation_repository import ReservationRepository
from src.application.validators import ensure_not_blank
from src.domain.entities.reservation import ReservationRecord


class ListReservationsUseCase:
    """Lists reservations for a customer."""

    def __init__(self, reservation_repo: ReservationRepository) -> None:
        self._reservation_repo = reservation_repo

    def execute(self, customer_id: str) -> List[ReservationRecord]:
        """Return reservations."""
        clean_customer_id = ensure_not_blank(customer_id, "customer_id")
        return self._reservation_repo.list_reservations_for_customer(clean_customer_id)
