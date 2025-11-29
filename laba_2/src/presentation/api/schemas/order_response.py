from pydantic import BaseModel


class OrderResponse(BaseModel):
    order_id: str
    status: str
    courier_id: str | None
    total_amount: float
