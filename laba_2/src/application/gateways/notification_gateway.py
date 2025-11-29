from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.entities.customer import Customer


class NotificationGateway(ABC):
    @abstractmethod
    def notify(self, customer: Customer, message: str) -> None:
        raise NotImplementedError
