from pydantic import BaseModel


class MenuItemResponse(BaseModel):
    item_id: str
    name: str
    price: float
