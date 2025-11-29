
from src.application.interfaces.services import IdentityProviderPort
from src.application.repositories.account_repository import AccountRepository
from src.application.validators import ensure_non_negative, ensure_not_blank
from src.domain.entities.customer import CustomerProfile
from src.errors.gallery_base_error import GalleryBaseError

class RegisterCustomerUseCase:

    def __init__(self, account_repo: AccountRepository, identity_provider: IdentityProviderPort) -> None:
        self._account_repo = account_repo
        self._identity_provider = identity_provider

    def execute(self, email: str, tier: str, balance: float) -> CustomerProfile:
        clean_email = ensure_not_blank(email, "email")
        is_existing = self._account_repo.get_customer_by_email(email)
        if is_existing:
            raise GalleryBaseError(error_code="404", message="castomer already exist")
        membership_tier = ensure_not_blank(tier, "tier")
        wallet_balance = ensure_non_negative(balance, "balance")
        customer = CustomerProfile(
            customer_id=self._identity_provider.generate_id("customer"),
            customer_email=clean_email,
            customer_membership_tier=membership_tier,
            customer_wallet_balance=wallet_balance,
        )
        customer.grant_role("customer")
        self._account_repo.save_customer(customer)
        return customer
