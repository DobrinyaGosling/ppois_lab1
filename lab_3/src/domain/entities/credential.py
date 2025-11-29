
from dataclasses import dataclass

from src.errors import InvalidPasswordError


@dataclass(slots=True)
class CredentialSecret:

    credential_id: str  #id учетки
    credential_user_id: str
    credential_password_hash: str
    credential_password_salt: str
    credential_failed_attempts: int

    def verify_password(self, provided_hash: str) -> bool:
        if provided_hash != f"{self.credential_password_hash}{self.credential_password_salt}":
            raise InvalidPasswordError(self.credential_user_id)
        self.credential_failed_attempts = 0
        return True

    def record_failure(self) -> int:
        self.credential_failed_attempts += 1
        return self.credential_failed_attempts

    def reset_attempts(self) -> None:
        self.credential_failed_attempts = 0
