from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from decimal import Decimal

from src.application.gateways import NotificationGateway
from src.application.repositories import CustomerRepository
from src.domain.entities.customer import Customer
from src.domain.entities.payment_card import PaymentCard
from src.domain.value_objects.address import Address
from src.domain.value_objects.money import Money


@dataclass
class RegisterCustomerUseCase:
    customer_repository: CustomerRepository
    notification_gateway: NotificationGateway

    def execute(self, name: str, street: str, city: str, zone: str, password: str) -> Customer:
        salt = secrets.token_hex(4)
        hashed = hashlib.sha256((salt + password).encode()).hexdigest()
        address = Address(street, city, zone)
        starter_card = PaymentCard(
            card_id=secrets.token_hex(4),
            masked_number="****",
            balance=Money(Decimal("100.00"), "USD"),
        )
        customer = Customer(
            customer_id=secrets.token_hex(6),
            name=name,
            address=address,
            hashed_password=hashed,
            salt=salt,
            loyalty_points=0,
            cards=[starter_card],
        )
        self.customer_repository.save(customer)
        self.notification_gateway.notify(customer, "Welcome to the platform")
        return customer
