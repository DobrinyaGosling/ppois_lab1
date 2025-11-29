
from dataclasses import dataclass

from src.errors import ReservationExpiredError


@dataclass(slots=True)
class ReservationRecord:

    reservation_id: str
    reservation_artwork_id: str
    reservation_customer_id: str
    reservation_expires_in_hours: int
    reservation_status_label: str
    reservation_private_view_flag: bool
    reservation_created_channel: str

    def mark_confirmed(self) -> str:
        self.reservation_status_label = "confirmed"
        return self.reservation_status_label

    def mark_expired(self) -> None:
        self.reservation_status_label = "expired"
        raise ReservationExpiredError(self.reservation_id)

    def extend_duration(self, extra_hours: int) -> int:
        self.reservation_expires_in_hours += extra_hours
        return self.reservation_expires_in_hours

    def can_auto_cancel(self) -> bool:
        return self.reservation_status_label == "pending" and not self.reservation_private_view_flag
