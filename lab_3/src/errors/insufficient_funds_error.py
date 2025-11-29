
from .gallery_base_error import GalleryBaseError


class InsufficientFundsError(GalleryBaseError):

    def __init__(self, customer_id: str) -> None:
        super().__init__("insufficient_funds", f"Customer {customer_id} has insufficient funds.")
