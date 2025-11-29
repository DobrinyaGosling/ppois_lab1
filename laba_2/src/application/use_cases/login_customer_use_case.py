from __future__ import annotations

import hashlib
from dataclasses import dataclass

from src.application.repositories import CustomerRepository
from src.exceptions import CustomerNotFoundError, InvalidPasswordError
from src.domain.entities.customer import Customer


@dataclass
class LoginCustomerUseCase:
    customer_repository: CustomerRepository

    def execute(self, name: str, password: str) -> Customer:
        customer = self.customer_repository.find_by_name(name)
        if not customer:
            raise CustomerNotFoundError(name)
        hashed = hashlib.sha256((customer.salt + password).encode()).hexdigest()
        if hashed != customer.hashed_password:
            raise InvalidPasswordError(customer.customer_id)
        return customer
