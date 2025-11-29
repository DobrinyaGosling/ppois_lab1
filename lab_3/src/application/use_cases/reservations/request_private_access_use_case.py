from src.application.repositories.account_repository import AccountRepository
from src.application.repositories.exhibition_repository import ExhibitionRepository
from src.application.validators import ensure_not_blank
from src.errors.exhibition_does_not_exist import ExhibitionDoesNotExist

class RequestPrivateAccessUseCase:

    def __init__(self, account_repo: AccountRepository, exhibition_repo: ExhibitionRepository) -> None:
        self._account_repo = account_repo
        self._exhibition_repo = exhibition_repo

    def execute(self, customer_id: str, exhibition_id: str) -> str:
        clean_customer_id = ensure_not_blank(customer_id, "customer_id")
        clean_exhibition_id = ensure_not_blank(exhibition_id, "exhibition_id")
        exhibition = self._exhibition_repo.get_exhibition(clean_exhibition_id)
        if exhibition is None:
            raise ExhibitionDoesNotExist(error_code="404")
        customer = self._account_repo.get_customer(clean_customer_id)
        if clean_exhibition_id not in customer.customer_preferred_exhibitions:
            customer.customer_preferred_exhibitions.append(clean_exhibition_id)
            self._account_repo.save_customer(customer)
        self._exhibition_repo.save_exhibition(exhibition)
        return "granted" if not exhibition.exhibition_private_flag else "pending"
