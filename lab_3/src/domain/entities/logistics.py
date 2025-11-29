"""Logistics ticket entity."""

from dataclasses import dataclass

from src.errors import LogisticsAssignmentError


@dataclass(slots=True)
class LogisticsTicket:

    logistics_ticket_id: str
    logistics_artwork_id: str
    logistics_origin_location: str
    logistics_destination_location: str
    logistics_scheduled_date: str
    logistics_courier_name: str
    logistics_status_label: str

    def assign_courier(self, courier_name: str) -> str:
        self.logistics_courier_name = courier_name
        return self.logistics_courier_name

    def mark_delivered(self) -> str:
        self.logistics_status_label = "delivered"
        return self.logistics_status_label

    def validate_assignment(self) -> None:
        if not self.logistics_courier_name:
            raise LogisticsAssignmentError(self.logistics_ticket_id)
