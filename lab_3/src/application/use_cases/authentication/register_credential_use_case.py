
from src.application.interfaces.services import IdentityProviderPort
from src.application.repositories.account_repository import AccountRepository
from src.application.validators import ensure_not_blank
from src.domain.entities.credential import CredentialSecret


class RegisterCredentialUseCase:

    def __init__(self, account_repo: AccountRepository, identity_provider: IdentityProviderPort) -> None:
        self._account_repo = account_repo
        self._identity_provider = identity_provider

    def execute(self, user_id: str, password_hash: str) -> CredentialSecret:
        clean_user_id = ensure_not_blank(user_id, "user_id")
        clean_hash = ensure_not_blank(password_hash, "password_hash")
        credential = CredentialSecret(
            credential_id=self._identity_provider.generate_id("cred"),
            credential_user_id=clean_user_id,
            credential_password_hash=clean_hash,
            credential_password_salt="salt",
            credential_failed_attempts=0,
        )
        self._account_repo.save_credential(credential)
        return credential
