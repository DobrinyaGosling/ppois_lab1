
from dataclasses import dataclass, field
from typing import List

from src.errors import InsufficientFundsError


@dataclass(slots=True)
class CustomerProfile:

    customer_id: str
    customer_email: str
    customer_membership_tier: str
    customer_wallet_balance: float
    customer_role_labels: List[str] = field(default_factory=list)
    customer_owned_artwork_ids: List[str] = field(default_factory=list)
    customer_preferred_exhibitions: List[str] = field(default_factory=list)

    def adjust_balance(self, delta: float) -> float:
        new_balance = self.customer_wallet_balance + delta
        if new_balance < 0:
            raise InsufficientFundsError(self.customer_id)
        self.customer_wallet_balance = new_balance
        return self.customer_wallet_balance

    def add_artwork_to_collection(self, artwork_id: str) -> int:
        if artwork_id not in self.customer_owned_artwork_ids:
            self.customer_owned_artwork_ids.append(artwork_id)
        return len(self.customer_owned_artwork_ids)

    def grant_role(self, role_name: str) -> int:
        if role_name not in self.customer_role_labels:
            self.customer_role_labels.append(role_name)
        return len(self.customer_role_labels)

    def wants_private_access(self, exhibition_id: str) -> bool:
        return exhibition_id in self.customer_preferred_exhibitions
