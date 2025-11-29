
from dataclasses import dataclass


@dataclass(slots=True)
class TransactionRecord:

    transaction_id: str
    transaction_artwork_id: str
    transaction_buyer_id: str
    transaction_amount_value: float
    transaction_payment_card_id: str
    transaction_status_label: str
    transaction_channel_code: str

    def mark_completed(self) -> str:
        self.transaction_status_label = "completed"
        return self.transaction_status_label

    def mark_failed(self) -> str:
        self.transaction_status_label = "failed"
        return self.transaction_status_label

    def summarize(self) -> str:
        return f"{self.transaction_id}:{self.transaction_status_label}:{self.transaction_amount_value}"
