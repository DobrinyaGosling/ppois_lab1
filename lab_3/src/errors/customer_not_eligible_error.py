
from .gallery_base_error import GalleryBaseError


class CustomerNotEligibleForPrivateViewingError(GalleryBaseError):

    def __init__(self, customer_id: str) -> None:
        super().__init__("private_view_denied", f"Customer {customer_id} is not eligible for private viewing.")
