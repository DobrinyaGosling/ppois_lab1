from src.application.repositories.account_repository import AccountRepository
from src.application.validators import ensure_not_blank
from src.errors.account_does_not_exist import AccountDoesNotExist

class LoginUseCase:
    def __init__(self, account_repo: AccountRepository) -> None:
        self._account_repo = account_repo

    def execute(self, user_id: str, provided_hash: str) -> bool:
        clean_user_id = ensure_not_blank(user_id, "user_id")
        clean_hash = ensure_not_blank(provided_hash, "password_hash")
        credential = self._account_repo.get_credential(clean_user_id)
        if credential is None:
            raise AccountDoesNotExist(error_code="404")
        salted = f"{clean_hash}{credential.credential_password_salt}"
        credential.verify_password(salted)
        self._account_repo.save_credential(credential)
        return True
