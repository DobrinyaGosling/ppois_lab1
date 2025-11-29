from __future__ import annotations

from typing import Dict, Optional

from src.application.repositories import CustomerRepository
from src.domain.entities.customer import Customer


class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self) -> None:
        self.customers: Dict[str, Customer] = {}

    def save(self, customer: Customer) -> None:
        self.customers[customer.customer_id] = customer

    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        return self.customers.get(customer_id)

    def find_by_name(self, name: str) -> Optional[Customer]:
        return next((c for c in self.customers.values() if c.name == name), None)
