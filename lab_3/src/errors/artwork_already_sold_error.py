
from .gallery_base_error import GalleryBaseError


class ArtworkAlreadySoldError(GalleryBaseError):

    def __init__(self, artwork_id: str) -> None:
        super().__init__("artwork_sold", f"Artwork {artwork_id} is already sold.")
