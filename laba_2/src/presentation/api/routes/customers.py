from fastapi import APIRouter, Depends

from src.application.use_cases import RegisterCustomerUseCase
from src.presentation.api.schemas import CustomerCreateRequest, CustomerResponse
from src.presentation.dependencies import get_register_customer_use_case

router = APIRouter()


@router.post("/customers", response_model=CustomerResponse)
def register_customer(
    payload: CustomerCreateRequest,
    use_case: RegisterCustomerUseCase = Depends(get_register_customer_use_case),
) -> CustomerResponse:
    customer = use_case.execute(payload.name, payload.street, payload.city, payload.zone, payload.password)
    return CustomerResponse(customer_id=customer.customer_id, name=customer.name, zone=customer.address.zone)
