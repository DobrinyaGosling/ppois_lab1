
from pydantic import BaseModel


class PrivateAccessRequestModel(BaseModel):

    customer_id: str

