"""Support service gateway implementations."""

from typing import Dict

from src.application.interfaces.services import InsuranceProviderPort, LogisticsProviderPort, PaymentGatewayPort


class SupportServiceGateway(PaymentGatewayPort, LogisticsProviderPort, InsuranceProviderPort):
    """In-memory adapter for payment, logistics, and insurance."""

    def __init__(self) -> None:
        self.support_authorizations: Dict[str, float] = {}
        self.support_logistics_status: Dict[str, str] = {}
        self.support_insurance_policies: Dict[str, float] = {}

    def authorize(self, payment_card_id: str, amount: float) -> str:
        code = f"auth-{payment_card_id}-{amount}"
        self.support_authorizations[code] = amount
        return code

    def capture(self, authorization_code: str) -> str:
        amount = self.support_authorizations.pop(authorization_code, 0.0)
        return f"captured-{authorization_code}-{amount}"

    def schedule_pickup(self, artwork_id: str, destination: str) -> str:
        logistics_id = f"log-{artwork_id}-{destination}"
        self.support_logistics_status[logistics_id] = "scheduled"
        return logistics_id

    def confirm_delivery(self, logistics_id: str) -> str:
        self.support_logistics_status[logistics_id] = "delivered"
        return self.support_logistics_status[logistics_id]

    def bind_policy(self, artwork_id: str, amount: float) -> str:
        policy_id = f"policy-{artwork_id}"
        self.support_insurance_policies[policy_id] = amount
        return policy_id

    def verify_policy(self, policy_id: str) -> bool:
        return policy_id in self.support_insurance_policies
