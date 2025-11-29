
from abc import ABC, abstractmethod


class PaymentGatewayPort(ABC):

    @abstractmethod
    def authorize(self, payment_card_id: str, amount: float) -> str: ...

    @abstractmethod
    def capture(self, authorization_code: str) -> str: ...


class LogisticsProviderPort(ABC):

    @abstractmethod
    def schedule_pickup(self, artwork_id: str, destination: str) -> str: ...

    @abstractmethod
    def confirm_delivery(self, logistics_id: str) -> str:...


class InsuranceProviderPort(ABC):

    @abstractmethod
    def bind_policy(self, artwork_id: str, amount: float) -> str: ...

    @abstractmethod
    def verify_policy(self, policy_id: str) -> bool: ...


class IdentityProviderPort(ABC):

    @abstractmethod
    def generate_id(self, prefix: str) -> str: ...
