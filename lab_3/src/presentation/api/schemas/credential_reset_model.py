
from pydantic import BaseModel


class CredentialResetModel(BaseModel):

    user_id: str

