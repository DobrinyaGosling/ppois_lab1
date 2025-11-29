from fastapi import APIRouter, Depends

from src.application.use_cases.catalog.calculate_collection_value_use_case import (
    CalculateCollectionValueUseCase,
)
from src.application.use_cases.catalog.get_customer_collection_use_case import (
    GetCustomerCollectionUseCase,
)
from src.application.use_cases.registration.assign_role_to_customer_use_case import (
    AssignRoleToCustomerUseCase,
)
from src.application.use_cases.registration.list_customer_roles_use_case import (
    ListCustomerRolesUseCase,
)
from src.application.use_cases.registration.user_registration_use_case import (
    RegistrationResult,
    UserRegistrationUseCase,
)
from src.presentation.api.schemas import RoleAssignmentModel, UserRegistrationModel
from src.presentation.dependencies import (
    get_assign_role_use_case,
    get_collection_value_use_case,
    get_customer_collection_use_case,
    get_list_customer_roles_use_case,
    get_user_registration_use_case,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
def register_user(
    payload: UserRegistrationModel,
    registration_uc: UserRegistrationUseCase = Depends(get_user_registration_use_case),
):
    result: RegistrationResult = registration_uc.execute(
        full_name=payload.full_name,
        preferred_medium=payload.preferred_medium,
        email=payload.email,
        tier=payload.tier,
        balance=payload.balance,
        password_hash=payload.password_hash,
    )
    if result["kind"] == "customer" and result["customer"] is not None:
        customer = result["customer"]
        return {"customer_id": customer.customer_id, "roles": customer.customer_role_labels}
    visitor = result["visitor"]
    return {"visitor_id": visitor.visitor_id, "preferred_medium": visitor.visitor_preferred_medium}


@router.get("/{customer_id}/collection")
def get_collection(
    customer_id: str,
    collection_uc: GetCustomerCollectionUseCase = Depends(get_customer_collection_use_case),
):
    collection = collection_uc.execute(customer_id)
    return {"customer_id": customer_id, "collection": collection}


@router.get("/{customer_id}/collection/value")
def get_collection_value(
    customer_id: str,
    value_uc: CalculateCollectionValueUseCase = Depends(get_collection_value_use_case),
):
    return {"customer_id": customer_id, "total_value": value_uc.execute(customer_id)}


@router.post("/{customer_id}/roles")
def assign_role(
    customer_id: str,
    payload: RoleAssignmentModel,
    assign_uc: AssignRoleToCustomerUseCase = Depends(get_assign_role_use_case),
):
    customer = assign_uc.execute(customer_id, payload.role_name)
    return {"customer_id": customer.customer_id, "roles": customer.customer_role_labels}


@router.get("/{customer_id}/roles")
def list_roles(
    customer_id: str,
    list_uc: ListCustomerRolesUseCase = Depends(get_list_customer_roles_use_case),
):
    return {"customer_id": customer_id, "roles": list_uc.execute(customer_id)}
