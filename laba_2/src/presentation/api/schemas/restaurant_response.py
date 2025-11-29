from pydantic import BaseModel


class RestaurantResponse(BaseModel):
    restaurant_id: str
    name: str
    zone: str
