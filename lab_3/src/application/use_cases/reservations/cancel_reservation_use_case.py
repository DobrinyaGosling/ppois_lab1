from src.application.repositories.catalog_repository import CatalogRepository
from src.application.repositories.reservation_repository import ReservationRepository
from src.application.validators import ensure_not_blank
from src.domain.entities.reservation import ReservationRecord
from src.errors.reservation_does_not_exist import ReservationDoesNotExist

class CancelReservationUseCase:

    def __init__(self, reservation_repo: ReservationRepository, catalog_repo: CatalogRepository) -> None:
        self._reservation_repo = reservation_repo
        self._catalog_repo = catalog_repo

    def execute(self, reservation_id: str) -> ReservationRecord:
        clean_reservation_id = ensure_not_blank(reservation_id, "reservation_id")
        reservation = self._reservation_repo.get_reservation(clean_reservation_id)
        if reservation is None:
            raise ReservationDoesNotExist(error_code="404")
        artwork = self._catalog_repo.get_artwork(reservation.reservation_artwork_id)
        reservation.reservation_status_label = "cancelled"
        artwork.update_status("available")
        self._reservation_repo.save_reservation(reservation)
        self._catalog_repo.save_artwork(artwork)
        return reservation
