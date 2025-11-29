
from fastapi import APIRouter, Depends

from src.application.use_cases.catalog.list_exhibitions_use_case import ListExhibitionsUseCase
from src.application.use_cases.reservations.request_private_access_use_case import RequestPrivateAccessUseCase
from src.presentation.api.schemas import PrivateAccessRequestModel
from src.presentation.dependencies import get_list_exhibitions_use_case, get_request_private_access_use_case

router = APIRouter(prefix="/exhibitions", tags=["exhibitions"])


@router.get("")
def list_exhibitions(
    list_uc: ListExhibitionsUseCase = Depends(get_list_exhibitions_use_case),
):
    exhibitions = list_uc.execute()
    return [
        {
            "exhibition_id": exh.exhibition_id,
            "name": exh.exhibition_name,
            "location": exh.exhibition_location,
            "capacity": exh.exhibition_capacity,
        }
        for exh in exhibitions
    ]


@router.post("/{exhibition_id}/private-access")
def request_private_access(
    exhibition_id: str,
    payload: PrivateAccessRequestModel,
    request_uc: RequestPrivateAccessUseCase = Depends(get_request_private_access_use_case),
):
    status = request_uc.execute(payload.customer_id, exhibition_id)
    return {"status": status}
