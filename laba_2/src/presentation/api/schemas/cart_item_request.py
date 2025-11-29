from pydantic import BaseModel


class CartItemRequest(BaseModel):
    customer_id: str
    restaurant_id: str
    item_id: str
    quantity: int
