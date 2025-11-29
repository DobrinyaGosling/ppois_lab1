
from .gallery_base_error import GalleryBaseError


class InsuranceValidationError(GalleryBaseError):

    def __init__(self, policy_id: str) -> None:
        super().__init__("insurance_invalid", f"Insurance policy {policy_id} is invalid.")
