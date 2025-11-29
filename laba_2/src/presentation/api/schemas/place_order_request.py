from pydantic import BaseModel


class PlaceOrderRequest(BaseModel):
    customer_id: str
    restaurant_id: str
    use_loyalty_points: int = 0
