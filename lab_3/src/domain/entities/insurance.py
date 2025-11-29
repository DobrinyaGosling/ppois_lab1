
from dataclasses import dataclass

from src.errors import InsuranceValidationError


@dataclass(slots=True)
class InsurancePolicy:

    insurance_policy_id: str
    insurance_artwork_id: str
    insurance_provider_name: str
    insurance_coverage_amount: float
    insurance_status_label: str
    insurance_expiration_date: str
    insurance_deductible_amount: float

    def activate(self) -> str:
        self.insurance_status_label = "active"
        return self.insurance_status_label

    def mark_expired(self) -> str:
        self.insurance_status_label = "expired"
        return self.insurance_status_label

    def adjust_coverage(self, delta: float) -> float:
        new_amount = self.insurance_coverage_amount + delta
        if new_amount <= 0:
            raise InsuranceValidationError(self.insurance_policy_id)
        self.insurance_coverage_amount = new_amount
        return self.insurance_coverage_amount
