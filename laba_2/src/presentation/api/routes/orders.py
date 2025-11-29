from fastapi import APIRouter, Depends

from src.application.use_cases import CancelOrderUseCase, GetOrderStatusUseCase, PlaceOrderUseCase
from src.presentation.api.schemas import OrderResponse, PlaceOrderRequest
from src.presentation.dependencies import (
    get_cancel_order_use_case,
    get_order_status_use_case,
    get_place_order_use_case,
)

router = APIRouter()


@router.post("/orders", response_model=OrderResponse)
def place_order(
    payload: PlaceOrderRequest,
    use_case: PlaceOrderUseCase = Depends(get_place_order_use_case),
) -> OrderResponse:
    order = use_case.execute(payload.customer_id, payload.restaurant_id, payload.use_loyalty_points)
    return OrderResponse(order_id=order.order_id, status=order.status, courier_id=order.courier_id, total_amount=float(order.total_amount.amount))


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: str,
    use_case: CancelOrderUseCase = Depends(get_cancel_order_use_case),
) -> OrderResponse:
    order = use_case.execute(order_id)
    return OrderResponse(order_id=order.order_id, status=order.status, courier_id=order.courier_id, total_amount=float(order.total_amount.amount))


@router.get("/orders/{order_id}/status")
def order_status(
    order_id: str,
    use_case: GetOrderStatusUseCase = Depends(get_order_status_use_case),
):
    status = use_case.execute(order_id)
    return {"order_id": order_id, "status": status}
