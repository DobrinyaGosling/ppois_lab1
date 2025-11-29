
from pydantic import BaseModel


class ReservationRequestModel(BaseModel):

    customer_id: str
    artwork_id: str
    private_view: bool = False

