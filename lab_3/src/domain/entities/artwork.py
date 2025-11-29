"""Artwork aggregate root."""

from dataclasses import dataclass, field
from typing import List

from src.errors import ArtworkAlreadySoldError, CustomerNotEligibleForPrivateViewingError


@dataclass(slots=True)
class Artwork:

    artwork_id: str
    artwork_title: str
    artwork_medium: str
    artwork_creation_year: int
    artwork_status_label: str
    artwork_dimensions_text: str
    artwork_artist_id: str
    artwork_appraisal_value: float
    artwork_reserved_customer_id: str | None = None
    artwork_private_view_roles: List[str] = field(default_factory=list)

    def mark_reserved(self, customer_id: str) -> None:
        self.artwork_reserved_customer_id = customer_id
        self.artwork_status_label = "reserved"

    def mark_sold(self, customer_id: str) -> None:
        if self.artwork_status_label == "sold":
            raise ArtworkAlreadySoldError(self.artwork_id)
        self.artwork_status_label = "sold"
        self.artwork_reserved_customer_id = customer_id

    def can_be_viewed_privately(self, customer_roles: List[str]) -> bool:
        if not set(customer_roles).intersection(set(self.artwork_private_view_roles)):
            raise CustomerNotEligibleForPrivateViewingError(self.artwork_id)
        return True

    def update_status(self, new_status: str) -> str:
        self.artwork_status_label = new_status
        return self.artwork_status_label
