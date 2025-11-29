import pytest
from fastapi import HTTPException

from src.presentation.api.schemas import (
    CredentialResetModel,
    LoginModel,
    PrivateAccessRequestModel,
    PurchaseRequestModel,
    ReservationRequestModel,
    RoleAssignmentModel,
    UserRegistrationModel,
)
from src.presentation.api.routes import artworks, auth, exhibitions, purchases, reservations, users
from src.presentation.dependencies import (
    get_artwork_detail_use_case,
    get_assign_role_use_case,
    get_cancel_reservation_use_case,
    get_collection_value_use_case,
    get_customer_collection_use_case,
    get_ensure_reservation_validity_use_case,
    get_list_artworks_use_case,
    get_list_exhibitions_use_case,
    get_list_reservations_use_case,
    get_list_customer_roles_use_case,
    get_purchase_artwork_use_case,
    get_request_private_access_use_case,
    get_reserve_artwork_use_case,
    get_reset_failed_attempts_use_case,
    get_user_registration_use_case,
    get_validate_password_use_case,
    reset_state,
)


def test_artwork_routes_return_data() -> None:
    reset_state()
    listing = artworks.list_artworks(list_uc=get_list_artworks_use_case())
    assert listing and listing[0]["artwork_id"].startswith("artwork")
    detail = artworks.get_artwork("artwork-1", detail_uc=get_artwork_detail_use_case())
    assert detail["artwork_id"] == "artwork-1"


def test_user_and_auth_routes() -> None:
    reset_state()
    payload = UserRegistrationModel(full_name="Zoe", preferred_medium="oil", password_hash="secret")
    response = users.register_user(
        payload,
        registration_uc=get_user_registration_use_case(),
    )
    assert "visitor_id" in response
    login_payload = LoginModel(user_id="customer-1", password_hash="secret")
    login_response = auth.login(login_payload, validate_uc=get_validate_password_use_case())
    assert login_response["status"] == "authenticated"
    auth.reset_attempts(
        CredentialResetModel(user_id="customer-1"),
        reset_uc=get_reset_failed_attempts_use_case(),
    )
    assigned = users.assign_role(
        "customer-1",
        RoleAssignmentModel(role_name="vip"),
        assign_uc=get_assign_role_use_case(),
    )
    assert "vip" in assigned["roles"]


def test_purchase_and_reservation_routes() -> None:
    reset_state()
    reservation_payload = ReservationRequestModel(customer_id="customer-1", artwork_id="artwork-2", private_view=True)
    reservation_response = reservations.create_reservation(
        reservation_payload,
        reserve_uc=get_reserve_artwork_use_case(),
    )
    assert reservation_response["status"] == "pending"
    purchase_payload = PurchaseRequestModel(customer_id="customer-1", artwork_id="artwork-1", payment_card_id="card-1")
    purchase_response = purchases.purchase_artwork(
        purchase_payload,
        purchase_uc=get_purchase_artwork_use_case(),
    )
    assert purchase_response["status"] == "completed"
    reservations.list_reservations(
        "customer-1",
        list_uc=get_list_reservations_use_case(),
    )
    reservations.cancel_reservation(
        reservation_response["reservation_id"],
        cancel_uc=get_cancel_reservation_use_case(),
    )


def test_exhibition_private_access_route() -> None:
    reset_state()
    private_payload = PrivateAccessRequestModel(customer_id="customer-1")
    status = exhibitions.request_private_access(
        "exhibit-1",
        private_payload,
        request_uc=get_request_private_access_use_case(),
    )
    assert status["status"] in {"granted", "pending"}


def test_list_exhibitions_and_collection_routes() -> None:
    reset_state()
    listing = exhibitions.list_exhibitions(list_uc=get_list_exhibitions_use_case())
    assert listing and listing[0]["exhibition_id"].startswith("exhibit")
    collection = users.get_collection(
        "customer-1",
        collection_uc=get_customer_collection_use_case(),
    )
    assert collection["collection"] == []
    total = users.get_collection_value(
        "customer-1",
        value_uc=get_collection_value_use_case(),
    )
    assert "total_value" in total
    roles = users.list_roles(
        "customer-1",
        list_uc=get_list_customer_roles_use_case(),
    )
    assert "roles" in roles


def test_reservation_validity_route_and_error_branch() -> None:
    reset_state()
    with pytest.raises(HTTPException):
        reservations.create_reservation(
            ReservationRequestModel(customer_id="customer-1", artwork_id="", private_view=False),
            reserve_uc=get_reserve_artwork_use_case(),
        )
    valid_payload = ReservationRequestModel(customer_id="customer-1", artwork_id="artwork-1", private_view=False)
    created = reservations.create_reservation(
        valid_payload,
        reserve_uc=get_reserve_artwork_use_case(),
    )
    validity = reservations.ensure_validity(
        created["reservation_id"],
        ensure_uc=get_ensure_reservation_validity_use_case(),
    )
    assert validity["valid"] is True
