from __future__ import annotations

from src.application.gateways import PaymentGateway
from src.domain.entities.customer import Customer
from src.domain.entities.order import Order
from src.exceptions import InsufficientFundsError


class InMemoryPaymentGateway(PaymentGateway):
    def charge(self, customer: Customer, order: Order) -> None:
        card = customer.primary_card()
        if not card:
            raise InsufficientFundsError("no-card")
        if card.balance.amount < order.total_amount.amount:
            raise InsufficientFundsError(card.card_id)
        card.charge(order.total_amount)

    def apply_loyalty(self, customer: Customer, amount: int) -> None:
        customer.add_points(amount)
