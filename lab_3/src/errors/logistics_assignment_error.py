
from .gallery_base_error import GalleryBaseError


class LogisticsAssignmentError(GalleryBaseError):

    def __init__(self, ticket_id: str) -> None:
        super().__init__("logistics_unavailable", f"Logistics ticket {ticket_id} cannot be processed.")
