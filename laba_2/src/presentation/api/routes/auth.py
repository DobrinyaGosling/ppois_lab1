from fastapi import APIRouter, Depends

from src.application.use_cases import LoginCustomerUseCase
from src.presentation.api.schemas import CustomerResponse, LoginRequest
from src.presentation.dependencies import get_login_customer_use_case

router = APIRouter()


@router.post("/auth/login", response_model=CustomerResponse)
def login(
    payload: LoginRequest,
    use_case: LoginCustomerUseCase = Depends(get_login_customer_use_case),
) -> CustomerResponse:
    customer = use_case.execute(payload.name, payload.password)
    return CustomerResponse(customer_id=customer.customer_id, name=customer.name, zone=customer.address.zone)
