"""Use case for retrieving a customer's collection."""

from typing import List

from src.application.repositories.account_repository import AccountRepository
from src.application.validators import ensure_not_blank
from src.errors.account_does_not_exist import AccountDoesNotExist

class GetCustomerCollectionUseCase:

    def __init__(self, account_repo: AccountRepository) -> None:
        self._account_repo = account_repo

    def execute(self, customer_id: str) -> List[str]:
        clean_customer_id = ensure_not_blank(customer_id, "customer_id")
        customer = self._account_repo.get_customer(clean_customer_id)
        if not customer:
            raise AccountDoesNotExist(error_code="404")
        return list(customer.customer_owned_artwork_ids)
