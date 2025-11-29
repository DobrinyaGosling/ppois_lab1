
from pydantic import BaseModel


class PurchaseRequestModel(BaseModel):

    customer_id: str
    artwork_id: str
    payment_card_id: str

