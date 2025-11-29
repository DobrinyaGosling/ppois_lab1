import pytest

from src.application.use_cases.authentication.reset_failed_attempts_use_case import (
    ResetFailedAttemptsUseCase,
)
from src.application.use_cases.authentication.validate_password_use_case import LoginUseCase
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
from src.application.use_cases.registration.register_customer_use_case import (
    RegisterCustomerUseCase,
)
from src.application.use_cases.reservations.cancel_reservation_use_case import (
    CancelReservationUseCase,
)
from src.application.use_cases.reservations.ensure_reservation_validity_use_case import (
    EnsureReservationValidityUseCase,
)
from src.application.use_cases.reservations.request_private_access_use_case import (
    RequestPrivateAccessUseCase,
)
from src.errors import GalleryBaseError
from src.errors.account_does_not_exist import AccountDoesNotExist
from src.errors.exhibition_does_not_exist import ExhibitionDoesNotExist
from src.errors.reservation_does_not_exist import ReservationDoesNotExist
from tests.test_use_cases import build_use_cases


def test_account_related_error_branches() -> None:
    deps = build_use_cases()
    reset_uc = ResetFailedAttemptsUseCase(deps["account_repo"])
    with pytest.raises(AccountDoesNotExist):
        reset_uc.execute("ghost-user")
    login_uc = LoginUseCase(deps["account_repo"])
    with pytest.raises(AccountDoesNotExist):
        login_uc.execute("ghost-user", "secret")
    collection_uc = GetCustomerCollectionUseCase(deps["account_repo"])
    with pytest.raises(AccountDoesNotExist):
        collection_uc.execute("ghost-user")
    value_uc = CalculateCollectionValueUseCase(deps["account_repo"], deps["catalog_repo"])
    with pytest.raises(AccountDoesNotExist):
        value_uc.execute("ghost-user")
    assign_uc = AssignRoleToCustomerUseCase(deps["account_repo"])
    with pytest.raises(AccountDoesNotExist):
        assign_uc.execute("ghost-user", "vip")
    list_uc = ListCustomerRolesUseCase(deps["account_repo"])
    with pytest.raises(AccountDoesNotExist):
        list_uc.execute("ghost-user")


def test_register_customer_duplicate_email_path() -> None:
    deps = build_use_cases()
    register_uc: RegisterCustomerUseCase = deps["register_customer"]
    register_uc.execute("dup@example.com", "silver", 1500.0)
    with pytest.raises(GalleryBaseError):
        register_uc.execute("dup@example.com", "gold", 800.0)
    found = deps["account_repo"].get_customer_by_email("dup@example.com")
    assert found is not None


def test_reservation_and_exhibition_missing_entities() -> None:
    deps = build_use_cases()
    cancel_uc = CancelReservationUseCase(deps["reservation_repo"], deps["catalog_repo"])
    with pytest.raises(ReservationDoesNotExist):
        cancel_uc.execute("missing-res")
    ensure_uc = EnsureReservationValidityUseCase(deps["reservation_repo"])
    with pytest.raises(ReservationDoesNotExist):
        ensure_uc.execute("missing-res")
    request_uc = RequestPrivateAccessUseCase(deps["account_repo"], deps["exhibition_repo"])
    customer = deps["register_customer"].execute("access@example.com", "silver", 1000.0)
    with pytest.raises(ExhibitionDoesNotExist):
        request_uc.execute(customer.customer_id, "missing-exhibit")


def test_reserve_artwork_missing_piece_triggers_error() -> None:
    deps = build_use_cases()
    customer = deps["register_customer"].execute("reserve@example.com", "gold", 4000.0)
    with pytest.raises(AccountDoesNotExist):
        deps["reserve"].execute(customer.customer_id, "missing-art", False)
