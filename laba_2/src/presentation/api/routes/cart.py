from fastapi import APIRouter, Depends

from src.application.use_cases import AddItemToCartUseCase, ApplyPromoUseCase, SummarizeCartUseCase
from src.presentation.api.schemas import CartItemRequest
from src.presentation.dependencies import (
    get_add_item_to_cart_use_case,
    get_apply_promo_use_case,
    get_summarize_cart_use_case,
)

router = APIRouter()


@router.post("/cart/items")
def add_cart_item(
    payload: CartItemRequest,
    use_case: AddItemToCartUseCase = Depends(get_add_item_to_cart_use_case),
):
    cart = use_case.execute(payload.customer_id, payload.restaurant_id, payload.item_id, payload.quantity)
    total = cart.total()
    return {"cart_id": cart.cart_id, "total": float(total.amount)}


@router.post("/cart/apply-promo")
def apply_promo(
    customer_id: str,
    restaurant_id: str,
    promo_code: str,
    use_case: ApplyPromoUseCase = Depends(get_apply_promo_use_case),
):
    cart = use_case.execute(customer_id, promo_code, restaurant_id)
    return {"cart_id": cart.cart_id, "promo_code": cart.promo_code}


@router.get("/cart/{customer_id}/summary")
def summarize_cart(
    customer_id: str,
    use_case: SummarizeCartUseCase = Depends(get_summarize_cart_use_case),
):
    total = use_case.execute(customer_id)
    return {"customer_id": customer_id, "total": float(total.amount)}
