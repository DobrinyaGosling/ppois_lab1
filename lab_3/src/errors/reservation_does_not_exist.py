
from .gallery_base_error import GalleryBaseError


class ReservationDoesNotExist(GalleryBaseError):

    def __init__(self, error_code) -> None:
        super().__init__(error_code, "Reservation does not exist")
