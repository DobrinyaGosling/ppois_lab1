
from .gallery_base_error import GalleryBaseError


class CuratorNotAuthorizedError(GalleryBaseError):

    def __init__(self, curator_id: str) -> None:
        super().__init__("curator_not_authorized", f"Curator {curator_id} is not authorized for this action.")
