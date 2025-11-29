"""Purchase routes."""

from fastapi import APIRouter, Depends

from src.application.use_cases.catalog.purchase_artwork_use_case import PurchaseArtworkUseCase
from src.presentation.api.schemas import PurchaseRequestModel
from src.presentation.dependencies import get_purchase_artwork_use_case

router = APIRouter(tags=["purchases"])


@router.post("/purchases")
def purchase_artwork(
    payload: PurchaseRequestModel,
    purchase_uc: PurchaseArtworkUseCase = Depends(get_purchase_artwork_use_case),
):
    transaction = purchase_uc.execute(payload.customer_id, payload.artwork_id, payload.payment_card_id)
    return {"transaction_id": transaction.transaction_id, "status": transaction.transaction_status_label}
