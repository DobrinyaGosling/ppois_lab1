
from .gallery_base_error import GalleryBaseError


class InvalidInputError(GalleryBaseError):

    def __init__(self, field_name: str, detail: str) -> None:
        super().__init__("invalid_input", f"{field_name}: {detail}")
