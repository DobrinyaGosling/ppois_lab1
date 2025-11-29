
from pydantic import BaseModel


class UserRegistrationModel(BaseModel):

    full_name: str
    preferred_medium: str
    email: str | None = None
    tier: str | None = None
    balance: float | None = None
    password_hash: str

