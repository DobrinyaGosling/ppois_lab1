from pydantic import BaseModel


class CustomerCreateRequest(BaseModel):
    name: str
    street: str
    city: str
    zone: str
    password: str
