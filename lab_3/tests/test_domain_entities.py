import pytest

from src.domain.entities.artwork import Artwork
from src.domain.entities.base_exhibition import Exhibition
from src.domain.entities.credential import CredentialSecret
from src.domain.entities.customer import CustomerProfile
from src.domain.entities.reservation import ReservationRecord
from src.errors import (
    ArtworkAlreadySoldError,
    CustomerNotEligibleForPrivateViewingError,
    InsufficientFundsError,
    InvalidPasswordError,
    ReservationExpiredError,
)


def test_artwork_private_view_and_sale() -> None:
    artwork = Artwork(
        artwork_id="art-1",
        artwork_title="Stone Path",
        artwork_medium="Stone",
        artwork_creation_year=2001,
        artwork_status_label="available",
        artwork_dimensions_text="20x40",
        artwork_artist_id="artist-test",
        artwork_appraisal_value=1000.0,
        artwork_private_view_roles=["collector"],
    )
    with pytest.raises(CustomerNotEligibleForPrivateViewingError):
        artwork.can_be_viewed_privately(["visitor"])
    assert artwork.can_be_viewed_privately(["collector"])
    artwork.mark_reserved("customer-1")
    artwork.mark_sold("customer-1")
    with pytest.raises(ArtworkAlreadySoldError):
        artwork.mark_sold("customer-2")
    artwork.update_status("inspection")
    assert artwork.artwork_status_label == "inspection"


def test_customer_wallet_adjustment_and_roles() -> None:
    customer = CustomerProfile(
        customer_id="cust-1",
        customer_email="cust@example.com",
        customer_membership_tier="gold",
        customer_wallet_balance=100.0,
    )
    customer.grant_role("collector")
    customer.add_artwork_to_collection("art-1")
    assert customer.adjust_balance(-50.0) == 50.0
    with pytest.raises(InsufficientFundsError):
        customer.adjust_balance(-100.0)
    customer.customer_preferred_exhibitions.append("exh-1")
    assert customer.wants_private_access("exh-1") is True


def test_reservation_expiration_logic() -> None:
    reservation = ReservationRecord(
        reservation_id="res-1",
        reservation_artwork_id="art-1",
        reservation_customer_id="cust-1",
        reservation_expires_in_hours=24,
        reservation_status_label="pending",
        reservation_private_view_flag=False,
        reservation_created_channel="api",
    )
    assert reservation.extend_duration(4) == 28
    assert reservation.can_auto_cancel() is True
    with pytest.raises(ReservationExpiredError):
        reservation.mark_expired()


def test_credentials_and_exhibition_flow() -> None:
    credential = CredentialSecret(
        credential_id="cred-1",
        credential_user_id="user-1",
        credential_password_hash="hash",
        credential_password_salt="salt",
        credential_failed_attempts=0,
    )
    credential.record_failure()
    with pytest.raises(InvalidPasswordError):
        credential.verify_password("wrong")
    credential.reset_attempts()
    assert credential.credential_failed_attempts == 0

    exhibition = Exhibition(
        exhibition_id="exh-10",
        exhibition_name="Hall Test",
        exhibition_location="Hall",
        exhibition_capacity=1,
        exhibition_curator_id="cur-1",
        exhibition_private_flag=False,
    )
    exhibition.add_artwork("art-1")
    exhibition.record_visit()
    exhibition.open_to_public()
