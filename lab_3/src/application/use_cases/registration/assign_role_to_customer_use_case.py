
from src.application.repositories.account_repository import AccountRepository
from src.application.validators import ensure_not_blank
from src.domain.entities.customer import CustomerProfile
from src.errors.account_does_not_exist import AccountDoesNotExist

class AssignRoleToCustomerUseCase:

    def __init__(self, account_repo: AccountRepository) -> None:
        self._account_repo = account_repo

    def execute(self, customer_id: str, role_name: str) -> CustomerProfile:
        clean_customer_id = ensure_not_blank(customer_id, "customer_id")
        clean_role = ensure_not_blank(role_name, "role_name")
        customer = self._account_repo.get_customer(clean_customer_id)
        if not customer:
            raise AccountDoesNotExist(error_code="404")
        customer.grant_role(clean_role)
        self._account_repo.save_customer(customer)
        return customer
