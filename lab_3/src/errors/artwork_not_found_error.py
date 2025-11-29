
from .gallery_base_error import GalleryBaseError


class ArtworkNotFoundError(GalleryBaseError):

    def __init__(self, artwork_id: str) -> None:
        super().__init__("artwork_not_found", f"Artwork {artwork_id} was not found.")
