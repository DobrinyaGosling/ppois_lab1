from pydantic import BaseModel


class CustomerResponse(BaseModel):
    customer_id: str
    name: str
    zone: str
