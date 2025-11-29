
from pydantic import BaseModel


class LoginModel(BaseModel):

    user_id: str
    password_hash: str

