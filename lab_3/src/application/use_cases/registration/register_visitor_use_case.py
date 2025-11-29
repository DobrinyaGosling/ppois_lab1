
from src.application.interfaces.services import IdentityProviderPort
from src.application.repositories.account_repository import AccountRepository
from src.application.validators import ensure_not_blank
from src.domain.entities.visitor import VisitorProfile


class RegisterVisitorUseCase:

    def __init__(self, account_repo: AccountRepository, identity_provider: IdentityProviderPort) -> None:
        self._account_repo = account_repo
        self._identity_provider = identity_provider

    def execute(self, full_name: str, preferred_medium: str) -> VisitorProfile:
        visitor_name = ensure_not_blank(full_name, "full_name")
        medium = ensure_not_blank(preferred_medium, "preferred_medium")
        visitor = VisitorProfile(
            visitor_id=self._identity_provider.generate_id("visitor"),
            visitor_full_name=visitor_name,
            visitor_preferred_medium=medium,
        )
        self._account_repo.save_visitor(visitor)
        return visitor
