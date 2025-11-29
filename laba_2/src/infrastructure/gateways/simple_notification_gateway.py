from __future__ import annotations

from src.application.gateways import NotificationGateway
from src.domain.entities.customer import Customer


class SimpleNotificationGateway(NotificationGateway):
    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def notify(self, customer: Customer, message: str) -> None:
        entry = f"{customer.customer_id}:{message}"
        self.sent_messages.append(entry)
