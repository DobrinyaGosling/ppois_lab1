
from src.application.interfaces.services import LogisticsProviderPort
from src.application.repositories.catalog_repository import CatalogRepository
from src.application.repositories.reservation_repository import ReservationRepository
from src.application.validators import ensure_not_blank
from src.domain.entities.reservation import ReservationRecord
from src.errors.account_does_not_exist import AccountDoesNotExist

class ReserveArtworkUseCase:

    def __init__(
        self,
        reservation_repo: ReservationRepository,
        catalog_repo: CatalogRepository,
        logistics_provider: LogisticsProviderPort,
    ) -> None:
        self._reservation_repo = reservation_repo
        self._catalog_repo = catalog_repo
        self._logistics_provider = logistics_provider

    def execute(self, customer_id: str, artwork_id: str, private_view: bool) -> ReservationRecord:
        clean_customer_id = ensure_not_blank(customer_id, "customer_id")
        clean_artwork_id = ensure_not_blank(artwork_id, "artwork_id")
        artwork = self._catalog_repo.get_artwork(clean_artwork_id)
        if artwork is None:
            raise AccountDoesNotExist(error_code="404")
        reservation = ReservationRecord(
            reservation_id=f"res-{clean_customer_id}-{clean_artwork_id}",
            reservation_artwork_id=clean_artwork_id,
            reservation_customer_id=clean_customer_id,
            reservation_expires_in_hours=24,
            reservation_status_label="pending",
            reservation_private_view_flag=private_view,
            reservation_created_channel="api",
        )
        artwork.mark_reserved(clean_customer_id)
        self._catalog_repo.save_artwork(artwork)
        self._reservation_repo.save_reservation(reservation)
        self._logistics_provider.schedule_pickup(clean_artwork_id, "viewing-room")
        return reservation
