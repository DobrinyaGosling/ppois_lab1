
from src.application.repositories.reservation_repository import ReservationRepository
from src.application.validators import ensure_not_blank
from src.errors import ReservationExpiredError
from src.errors.reservation_does_not_exist import ReservationDoesNotExist


class EnsureReservationValidityUseCase:

    def __init__(self, reservation_repo: ReservationRepository) -> None:
        self._reservation_repo = reservation_repo

    def execute(self, reservation_id: str) -> bool:
        clean_reservation_id = ensure_not_blank(reservation_id, "reservation_id")
        reservation = self._reservation_repo.get_reservation(clean_reservation_id)
        if reservation is None:
            raise ReservationDoesNotExist(error_code="404")
        if reservation.reservation_status_label == "expired":
            raise ReservationExpiredError(reservation_id)
        return True
