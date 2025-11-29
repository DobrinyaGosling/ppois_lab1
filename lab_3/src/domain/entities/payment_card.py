"""Payment card entity."""

from dataclasses import dataclass

from src.errors import PaymentAuthorizationError


@dataclass(slots=True)
class PaymentCard:

    payment_card_id: str
    payment_card_customer_id: str
    payment_card_masked_number: str
    payment_card_expiration_month: int
    payment_card_expiration_year: int
    payment_card_security_token: str
    payment_card_daily_limit: float

    def authorize_amount(self, amount: float) -> float:
        if amount > self.payment_card_daily_limit:
            raise PaymentAuthorizationError(self.payment_card_id)
        self.payment_card_daily_limit -= amount
        return self.payment_card_daily_limit

    def release_amount(self, amount: float) -> float:
        self.payment_card_daily_limit += amount
        return self.payment_card_daily_limit

    def mask_number(self) -> str:
        return f"****{self.payment_card_masked_number[-4:]}"
