from fastapi import APIRouter, Depends

from src.application.use_cases import GetRestaurantMenuUseCase, ListRestaurantsUseCase
from src.presentation.api.schemas import MenuItemResponse, RestaurantResponse
from src.presentation.dependencies import get_list_restaurants_use_case, get_menu_use_case

router = APIRouter()


@router.get("/restaurants", response_model=list[RestaurantResponse])
def list_restaurants(
    use_case: ListRestaurantsUseCase = Depends(get_list_restaurants_use_case),
) -> list[RestaurantResponse]:
    restaurants = use_case.execute()
    return [RestaurantResponse(restaurant_id=r.restaurant_id, name=r.name, zone=r.address.zone) for r in restaurants]


@router.get("/restaurants/{restaurant_id}/menu", response_model=list[MenuItemResponse])
def get_menu(
    restaurant_id: str,
    use_case: GetRestaurantMenuUseCase = Depends(get_menu_use_case),
) -> list[MenuItemResponse]:
    menu = use_case.execute(restaurant_id)
    return [MenuItemResponse(item_id=m.item_id, name=m.name, price=float(m.price.amount)) for m in menu]
