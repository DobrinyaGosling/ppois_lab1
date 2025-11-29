
from .gallery_base_error import GalleryBaseError


class PaymentAuthorizationError(GalleryBaseError):

    def __init__(self, transaction_id: str) -> None:
        super().__init__("payment_authorization_failed", f"Payment authorization failed for {transaction_id}.")
