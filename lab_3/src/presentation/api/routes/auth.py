from fastapi import APIRouter, Depends

from src.application.use_cases.authentication.reset_failed_attempts_use_case import (
    ResetFailedAttemptsUseCase,
)
from src.application.use_cases.authentication.validate_password_use_case import (
    LoginUseCase,
)
from src.presentation.api.schemas import CredentialResetModel, LoginModel
from src.presentation.dependencies import (
    get_reset_failed_attempts_use_case,
    get_validate_password_use_case,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    payload: LoginModel,
    validate_uc: LoginUseCase = Depends(get_validate_password_use_case),
):
    validate_uc.execute(payload.user_id, payload.password_hash)
    return {"status": "authenticated"}


@router.post("/reset")
def reset_attempts(
    payload: CredentialResetModel,
    reset_uc: ResetFailedAttemptsUseCase = Depends(get_reset_failed_attempts_use_case),
):
    reset_uc.execute(payload.user_id)
    return {"status": "reset"}
