from dataclasses import dataclass
from typing import Literal, TypedDict

from src.application.use_cases.registration.register_customer_use_case import RegisterCustomerUseCase
from src.application.use_cases.registration.register_visitor_use_case import RegisterVisitorUseCase
from src.application.use_cases.authentication.register_credential_use_case import RegisterCredentialUseCase
from src.domain.entities.customer import CustomerProfile
from src.domain.entities.visitor import VisitorProfile


class RegistrationResult(TypedDict):
    kind: Literal["customer", "visitor"]
    customer: CustomerProfile | None
    visitor: VisitorProfile | None


@dataclass(slots=True)
class UserRegistrationUseCase:
    register_customer_use_case: RegisterCustomerUseCase
    register_visitor_use_case: RegisterVisitorUseCase
    register_credential_use_case: RegisterCredentialUseCase

    def execute(
        self,
        full_name: str,
        preferred_medium: str,
        email: str | None,
        tier: str | None,
        balance: float | None,
        password_hash: str,
    ) -> RegistrationResult:
        if email and tier is not None:
            customer = self.register_customer_use_case.execute(email, tier, balance or 0.0)
            self.register_credential_use_case.execute(customer.customer_id, password_hash)
            return RegistrationResult(kind="customer", customer=customer, visitor=None)

        visitor = self.register_visitor_use_case.execute(full_name, preferred_medium)
        return RegistrationResult(kind="visitor", customer=None, visitor=visitor)
