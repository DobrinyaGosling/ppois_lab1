
from .gallery_base_error import GalleryBaseError


class ReservationExpiredError(GalleryBaseError):

    def __init__(self, reservation_id: str) -> None:
        super().__init__("reservation_expired", f"Reservation {reservation_id} expired.")
