
from .gallery_base_error import GalleryBaseError


class InvalidPasswordError(GalleryBaseError):

    def __init__(self, username: str) -> None:
        super().__init__("invalid_password", f"Password validation failed for {username}.")
