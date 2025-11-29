
from .gallery_base_error import GalleryBaseError


class ExhibitionDoesNotExist(GalleryBaseError):

    def __init__(self, error_code) -> None:
        super().__init__(error_code, "exhibition does not exist")
