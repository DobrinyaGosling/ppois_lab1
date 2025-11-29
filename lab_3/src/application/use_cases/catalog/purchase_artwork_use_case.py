
from src.application.interfaces.services import InsuranceProviderPort, LogisticsProviderPort, PaymentGatewayPort
from src.application.repositories.account_repository import AccountRepository
from src.application.repositories.catalog_repository import CatalogRepository
from src.application.validators import ensure_not_blank
from src.domain.entities.transaction import TransactionRecord


class PurchaseArtworkUseCase:

    def __init__(
        self,
        catalog_repo: CatalogRepository,
        account_repo: AccountRepository,
        payment_gateway: PaymentGatewayPort,
        insurance_provider: InsuranceProviderPort,
        logistics_provider: LogisticsProviderPort,
    ) -> None:
        self._catalog_repo = catalog_repo
        self._account_repo = account_repo
        self._payment_gateway = payment_gateway
        self._insurance_provider = insurance_provider
        self._logistics_provider = logistics_provider

    def execute(self, customer_id: str, artwork_id: str, payment_card_id: str) -> TransactionRecord:
        clean_customer_id = ensure_not_blank(customer_id, "customer_id")
        clean_artwork_id = ensure_not_blank(artwork_id, "artwork_id")
        clean_card_id = ensure_not_blank(payment_card_id, "payment_card_id")
        artwork = self._catalog_repo.get_artwork(clean_artwork_id)
        customer = self._account_repo.get_customer(clean_customer_id)
        authorization_code = self._payment_gateway.authorize(clean_card_id, artwork.artwork_appraisal_value)
        self._payment_gateway.capture(authorization_code)
        policy_id = self._insurance_provider.bind_policy(clean_artwork_id, artwork.artwork_appraisal_value)
        logistics_id = self._logistics_provider.schedule_pickup(clean_artwork_id, "customer-address")
        artwork.mark_sold(clean_customer_id)
        customer.adjust_balance(-artwork.artwork_appraisal_value)
        customer.add_artwork_to_collection(clean_artwork_id)
        transaction = TransactionRecord(
            transaction_id=f"txn-{clean_artwork_id}-{clean_customer_id}",
            transaction_artwork_id=clean_artwork_id,
            transaction_buyer_id=clean_customer_id,
            transaction_amount_value=artwork.artwork_appraisal_value,
            transaction_payment_card_id=clean_card_id,
            transaction_status_label="completed",
            transaction_channel_code="online",
        )
        self._account_repo.save_customer(customer)
        self._catalog_repo.save_artwork(artwork)
        self._account_repo.save_transaction_record(transaction)
        self._logistics_provider.confirm_delivery(logistics_id)
        self._insurance_provider.verify_policy(policy_id)
        return transaction
