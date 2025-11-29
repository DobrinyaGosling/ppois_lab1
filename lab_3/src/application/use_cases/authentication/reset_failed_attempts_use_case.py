
from src.application.repositories.account_repository import AccountRepository
from src.application.validators import ensure_not_blank
from src.errors.account_does_not_exist import AccountDoesNotExist

class ResetFailedAttemptsUseCase:

    def __init__(self, account_repo: AccountRepository) -> None:
        self._account_repo = account_repo

    def execute(self, user_id: str) -> int:
        clean_user_id = ensure_not_blank(user_id, "user_id")
        credential = self._account_repo.get_credential(clean_user_id)
        if not credential:
            raise AccountDoesNotExist(error_code="404")
        credential.reset_attempts()
        self._account_repo.save_credential(credential)
        return credential.credential_failed_attempts
