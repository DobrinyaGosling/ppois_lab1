
from .gallery_base_error import GalleryBaseError


class ExhibitionClosedError(GalleryBaseError):

    def __init__(self, exhibition_id: str) -> None:
        super().__init__("exhibition_closed", f"Exhibition {exhibition_id} is closed.")
