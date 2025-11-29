
from src.application.repositories.account_repository import AccountRepository
from src.application.repositories.catalog_repository import CatalogRepository
from src.application.validators import ensure_not_blank
from src.errors.account_does_not_exist import AccountDoesNotExist

class CalculateCollectionValueUseCase:

    def __init__(self, account_repo: AccountRepository, catalog_repo: CatalogRepository) -> None:
        self._account_repo = account_repo
        self._catalog_repo = catalog_repo

    def execute(self, customer_id: str) -> float:
        clean_customer_id = ensure_not_blank(customer_id, "customer_id")
        customer = self._account_repo.get_customer(clean_customer_id)
        if not customer:
            raise AccountDoesNotExist(error_code="404")
        total = 0.0
        for artwork_id in customer.customer_owned_artwork_ids:
            artwork = self._catalog_repo.get_artwork(artwork_id)
            total += artwork.artwork_appraisal_value
        return total
