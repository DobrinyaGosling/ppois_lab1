
from .gallery_base_error import GalleryBaseError


class ProvenanceVerificationError(GalleryBaseError):

    def __init__(self, artwork_id: str) -> None:
        super().__init__("provenance_invalid", f"Provenance chain incomplete for artwork {artwork_id}.")
