from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.customer import Customer


class CustomerRepository(ABC):
    @abstractmethod
    def save(self, customer: Customer) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Customer]:
        raise NotImplementedError
