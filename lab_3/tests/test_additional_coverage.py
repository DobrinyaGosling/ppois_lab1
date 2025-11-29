import pytest

from src.application.use_cases.catalog.calculate_collection_value_use_case import CalculateCollectionValueUseCase
from src.application.use_cases.catalog.get_artwork_detail_use_case import GetArtworkDetailUseCase
from src.application.use_cases.catalog.get_customer_collection_use_case import GetCustomerCollectionUseCase
from src.application.use_cases.catalog.list_exhibitions_use_case import ListExhibitionsUseCase
from src.application.use_cases.registration.assign_role_to_customer_use_case import AssignRoleToCustomerUseCase
from src.application.use_cases.registration.list_customer_roles_use_case import ListCustomerRolesUseCase
from src.application.use_cases.reservations.cancel_reservation_use_case import CancelReservationUseCase
from src.application.use_cases.reservations.ensure_reservation_validity_use_case import EnsureReservationValidityUseCase
from src.application.use_cases.reservations.list_reservations_use_case import ListReservationsUseCase
from src.application.use_cases.reservations.request_private_access_use_case import RequestPrivateAccessUseCase
from src.domain.entities.base_exhibition import Exhibition
from src.domain.entities.public_exhibition import PublicExhibition
from src.domain.entities.transaction import TransactionRecord
from src.domain.entities.visitor import VisitorProfile
from src.errors import (
    ArtworkNotFoundError,
    CuratorNotAuthorizedError,
    CustomerNotEligibleForPrivateViewingError,
    InsufficientFundsError,
    LogisticsAssignmentError,
    ReservationExpiredError,
    PaymentAuthorizationError,
)
from src.presentation.api.schemas import UserRegistrationModel
from src.presentation.api.routes import users
from src.presentation.dependencies import get_user_registration_use_case, reset_state
from tests.test_use_cases import build_use_cases


def test_catalog_additional_behaviors() -> None:
    deps = build_use_cases()
    customer = deps["register_customer"].execute("collector@example.com", "gold", 6000.0)
    deps["register_credential"].execute(customer.customer_id, "hash")
    list_exh_uc = ListExhibitionsUseCase(deps["exhibition_repo"])
    assert list_exh_uc.execute()
    collection_uc = GetCustomerCollectionUseCase(deps["account_repo"])
    assert collection_uc.execute(customer.customer_id) == []
    value_uc = CalculateCollectionValueUseCase(deps["account_repo"], deps["catalog_repo"])
    assert value_uc.execute(customer.customer_id) == 0.0
    request_private_uc = RequestPrivateAccessUseCase(deps["account_repo"], deps["exhibition_repo"])
    request_private_uc.execute(customer.customer_id, "exhibit-usecase")
    reservation = deps["reserve"].execute(customer.customer_id, "art-usecase", False)
    ensure_uc = EnsureReservationValidityUseCase(deps["reservation_repo"])
    ensure_uc.execute(reservation.reservation_id)
    cancel_uc = CancelReservationUseCase(deps["reservation_repo"], deps["catalog_repo"])
    cancel_uc.execute(reservation.reservation_id)
    list_res_uc = ListReservationsUseCase(deps["reservation_repo"])
    assert isinstance(list_res_uc.execute(customer.customer_id), list)
    deps["account_repo"].get_customer(customer.customer_id).customer_owned_artwork_ids.append("art-usecase")
    assert value_uc.execute(customer.customer_id) > 0.0


def test_user_registration_role_management() -> None:
    deps = build_use_cases()
    customer = deps["register_customer"].execute("role@example.com", "silver", 2000.0)
    assign_uc = AssignRoleToCustomerUseCase(deps["account_repo"])
    assign_uc.execute(customer.customer_id, "vip")
    list_roles_uc = ListCustomerRolesUseCase(deps["account_repo"])
    roles = list_roles_uc.execute(customer.customer_id)
    assert "vip" in roles


def test_domain_entities_extended_methods() -> None:
    exhibition = Exhibition(
        exhibition_id="exh-1",
        exhibition_name="Expo",
        exhibition_location="Hall",
        exhibition_capacity=1,
        exhibition_curator_id="cur-1",
        exhibition_private_flag=False,
    )
    exhibition.add_artwork("art-1")
    exhibition.record_visit()
    public_exhibition = PublicExhibition(
        exhibition_id="exh-2",
        exhibition_name="Public",
        exhibition_location="Main",
        exhibition_capacity=50,
        exhibition_curator_id="cur-2",
        exhibition_private_flag=False,
    )
    public_exhibition.apply_discount(0.1)
    public_exhibition.assign_language("es")
    public_exhibition.schedule_guided_tours(5)


def test_transaction_and_visitor_helpers() -> None:
    transaction = TransactionRecord(
        transaction_id="txn-1",
        transaction_artwork_id="art-1",
        transaction_buyer_id="cust-1",
        transaction_amount_value=100.0,
        transaction_payment_card_id="card-1",
        transaction_status_label="pending",
        transaction_channel_code="online",
    )
    transaction.mark_completed()
    transaction.mark_failed()
    assert transaction.summarize().startswith("txn-1")
    visitor = VisitorProfile(
        visitor_id="vis-1",
        visitor_full_name="Visitor",
        visitor_preferred_medium="oil",
    )
    visitor.add_feedback("great")
    visitor.add_reservation("res-1")
    visitor.redeem_points(5)


def test_error_classes_raise_with_messages() -> None:
    with pytest.raises(PaymentAuthorizationError):
        raise PaymentAuthorizationError("txn")
    with pytest.raises(LogisticsAssignmentError):
        raise LogisticsAssignmentError("ticket")
    with pytest.raises(CuratorNotAuthorizedError):
        raise CuratorNotAuthorizedError("curator")
    with pytest.raises(CustomerNotEligibleForPrivateViewingError):
        raise CustomerNotEligibleForPrivateViewingError("cust")
    with pytest.raises(InsufficientFundsError):
        raise InsufficientFundsError("cust")


def test_user_route_customer_branch() -> None:
    reset_state()
    registration_uc = get_user_registration_use_case()
    registration_payload = UserRegistrationModel(
        full_name="Collector",
        preferred_medium="oil",
        email="collector@example.com",
        tier="gold",
        balance=9000.0,
        password_hash="hash",
    )
    response = users.register_user(
        registration_payload,
        registration_uc=registration_uc,
    )
    assert "customer_id" in response


def test_artwork_detail_error_path() -> None:
    deps = build_use_cases()
    detail_uc = GetArtworkDetailUseCase(deps["catalog_repo"])
    with pytest.raises(ArtworkNotFoundError):
        detail_uc.execute("missing-art")


def test_reservation_validity_error_path() -> None:
    deps = build_use_cases()
    reservation = deps["reserve"].execute("customer-1", "art-usecase", False)
    deps["reservation_repo"].reservation_storage_map[reservation.reservation_id].reservation_status_label = "expired"
    ensure_uc = EnsureReservationValidityUseCase(deps["reservation_repo"])
    with pytest.raises(ReservationExpiredError):
        ensure_uc.execute(reservation.reservation_id)
