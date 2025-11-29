
from .gallery_base_error import GalleryBaseError


class AccountDoesNotExist(GalleryBaseError):

    def __init__(self, error_code) -> None:
        super().__init__(error_code, "account does not existor_code")
