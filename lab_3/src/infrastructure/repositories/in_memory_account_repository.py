
from typing import Dict, List

from src.application.repositories.account_repository import AccountRepository
from src.domain.entities.credential import CredentialSecret
from src.domain.entities.customer import CustomerProfile
from src.domain.entities.transaction import TransactionRecord
from src.domain.entities.visitor import VisitorProfile


class InMemoryAccountRepository(AccountRepository):

    def __init__(self) -> None:
        self.account_storage_customers: Dict[str, CustomerProfile] = {}
        self.customer_email_index: Dict[str, str] = {}
        self.account_storage_visitors: Dict[str, VisitorProfile] = {}
        self.account_storage_credentials: Dict[str, CredentialSecret] = {}
        self.account_storage_transactions: List[TransactionRecord] = []

    def save_customer(self, customer: CustomerProfile) -> None:
        self.account_storage_customers[customer.customer_id] = customer
        self.customer_email_index[customer.customer_email] = customer.customer_id

    def save_visitor(self, visitor: VisitorProfile) -> None:
        self.account_storage_visitors[visitor.visitor_id] = visitor

    def get_customer(self, customer_id: str) -> CustomerProfile | None:
        return self.account_storage_customers.get(customer_id)

    def get_customer_by_email(self, email: str) -> CustomerProfile | None:
        customer_id = self.customer_email_index.get(email)
        if customer_id is not None:
            return self.account_storage_customers.get(customer_id)
        return None

    def get_visitor(self, visitor_id: str) -> VisitorProfile | None:
        return self.account_storage_visitors.get(visitor_id)

    def save_credential(self, credential: CredentialSecret) -> None:
        self.account_storage_credentials[credential.credential_user_id] = credential

    def get_credential(self, user_id: str) -> CredentialSecret | None:
        return self.account_storage_credentials.get(user_id)

    def save_transaction_record(self, transaction: TransactionRecord) -> None:
        self.account_storage_transactions.append(transaction)

    def list_transactions_for_customer(self, customer_id: str) -> List[TransactionRecord]:
        return [txn for txn in self.account_storage_transactions if txn.transaction_buyer_id == customer_id]
