
from fastapi import APIRouter, Depends, HTTPException

from src.application.use_cases.reservations.cancel_reservation_use_case import CancelReservationUseCase
from src.application.use_cases.reservations.ensure_reservation_validity_use_case import (
    EnsureReservationValidityUseCase,
)
from src.application.use_cases.reservations.list_reservations_use_case import ListReservationsUseCase
from src.application.use_cases.reservations.reserve_artwork_use_case import ReserveArtworkUseCase
from src.presentation.api.schemas import ReservationRequestModel
from src.presentation.dependencies import (
    get_cancel_reservation_use_case,
    get_ensure_reservation_validity_use_case,
    get_list_reservations_use_case,
    get_reserve_artwork_use_case,
)

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("")
def create_reservation(
    payload: ReservationRequestModel,
    reserve_uc: ReserveArtworkUseCase = Depends(get_reserve_artwork_use_case),
):
    if not payload.artwork_id:
        raise HTTPException(status_code=400, detail="artwork_id required")
    reservation = reserve_uc.execute(payload.customer_id, payload.artwork_id, payload.private_view)
    return {"reservation_id": reservation.reservation_id, "status": reservation.reservation_status_label}


@router.get("/customer/{customer_id}")
def list_reservations(
    customer_id: str,
    list_uc: ListReservationsUseCase = Depends(get_list_reservations_use_case),
):
    reservations = list_uc.execute(customer_id)
    return [
        {"reservation_id": res.reservation_id, "status": res.reservation_status_label}
        for res in reservations
    ]


@router.delete("/{reservation_id}")
def cancel_reservation(
    reservation_id: str,
    cancel_uc: CancelReservationUseCase = Depends(get_cancel_reservation_use_case),
):
    reservation = cancel_uc.execute(reservation_id)
    return {"reservation_id": reservation.reservation_id, "status": reservation.reservation_status_label}


@router.get("/{reservation_id}/valid")
def ensure_validity(
    reservation_id: str,
    ensure_uc: EnsureReservationValidityUseCase = Depends(get_ensure_reservation_validity_use_case),
):
    ensure_uc.execute(reservation_id)
    return {"reservation_id": reservation_id, "valid": True}
