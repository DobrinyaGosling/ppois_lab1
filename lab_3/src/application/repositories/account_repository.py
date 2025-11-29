
from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.credential import CredentialSecret
from src.domain.entities.customer import CustomerProfile
from src.domain.entities.transaction import TransactionRecord
from src.domain.entities.visitor import VisitorProfile


class AccountRepository(ABC):

    @abstractmethod
    def save_customer(self, customer: CustomerProfile) -> None: ...

    @abstractmethod
    def save_visitor(self, visitor: VisitorProfile) -> None: ...

    @abstractmethod
    def get_customer(self, customer_id: str) -> CustomerProfile | None: ...

    @abstractmethod
    def get_customer_by_email(self, email: str) -> CustomerProfile | None: ...

    @abstractmethod
    def get_visitor(self, visitor_id: str) -> VisitorProfile | None: ...

    @abstractmethod
    def save_credential(self, credential: CredentialSecret) -> None: ...

    @abstractmethod
    def get_credential(self, user_id: str) -> CredentialSecret | None: ...

    @abstractmethod
    def save_transaction_record(self, transaction: TransactionRecord) -> None: ...

    @abstractmethod
    def list_transactions_for_customer(self, customer_id: str) -> List[TransactionRecord]: ...
