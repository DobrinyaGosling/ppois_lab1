import pytest

from src.application.use_cases.authentication.register_credential_use_case import RegisterCredentialUseCase
from src.application.use_cases.registration.register_customer_use_case import RegisterCustomerUseCase
from src.application.use_cases.registration.register_visitor_use_case import RegisterVisitorUseCase
from src.application.validators import ensure_non_negative, ensure_not_blank, ensure_positive
from src.domain.entities.artist import Artist
from src.domain.entities.base_exhibition import Exhibition
from src.domain.entities.credential import CredentialSecret
from src.domain.entities.customer import CustomerProfile
from src.domain.entities.insurance import InsurancePolicy
from src.domain.entities.logistics import LogisticsTicket
from src.domain.entities.reservation import ReservationRecord
from src.domain.entities.transaction import TransactionRecord
from src.domain.entities.visitor import VisitorProfile
from src.errors import (
    ExhibitionClosedError,
    GalleryBaseError,
    InsuranceValidationError,
    InvalidInputError,
    LogisticsAssignmentError,
    ProvenanceVerificationError,
    ReservationExpiredError,
)
from src.infrastructure.repositories.in_memory_account_repository import InMemoryAccountRepository
from src.presentation import dependencies


def test_string_and_numeric_validators_cover_all_paths() -> None:
    assert ensure_not_blank("  value  ", "field") == "value"
    assert ensure_non_negative(0.0, "amount") == 0.0
    assert ensure_positive(1.0, "amount") == 1.0
    with pytest.raises(InvalidInputError):
        ensure_not_blank("   ", "field")
    with pytest.raises(InvalidInputError):
        ensure_not_blank(None, "field")  # type: ignore[arg-type]
    with pytest.raises(InvalidInputError):
        ensure_non_negative(-1, "amount")
    with pytest.raises(InvalidInputError):
        ensure_positive(0, "amount")
    with pytest.raises(InvalidInputError):
        ensure_non_negative(None, "amount")  # type: ignore[arg-type]
    with pytest.raises(InvalidInputError):
        ensure_positive(None, "amount")  # type: ignore[arg-type]


def test_artist_catalog_management_and_biography_updates() -> None:
    artist = Artist(
        artist_id="artist-1",
        artist_stage_name="Aura",
        artist_nationality="BY",
        artist_biography_text="Bio",
        artist_signature_style="Modern",
    )
    assert artist.add_award("Golden Brush") == 1
    assert artist.add_award("Golden Brush") == 1
    artist.update_biography("Updated")
    assert artist.artist_biography_text == "Updated"
    artist.attach_artwork("art-1")
    artist.attach_artwork("art-1")
    assert artist.artist_artwork_ids == ["art-1"]


def test_exhibition_capacity_reset_and_full_detection() -> None:
    exhibition = Exhibition(
        exhibition_id="exh-1",
        exhibition_name="Avant",
        exhibition_location="Hall A",
        exhibition_capacity=1,
        exhibition_curator_id="cur-1",
        exhibition_private_flag=False,
    )
    assert exhibition.record_visit() == 1
    assert exhibition.is_full() is True
    with pytest.raises(ExhibitionClosedError):
        exhibition.record_visit()
    exhibition.open_to_public()
    assert exhibition.exhibition_attendance_count == 0


def test_reservation_lifecycle_and_expiry_signal() -> None:
    reservation = ReservationRecord(
        reservation_id="res-1",
        reservation_artwork_id="art-1",
        reservation_customer_id="cust-1",
        reservation_expires_in_hours=4,
        reservation_status_label="pending",
        reservation_private_view_flag=False,
        reservation_created_channel="web",
    )
    reservation.extend_duration(2)
    assert reservation.reservation_expires_in_hours == 6
    reservation.mark_confirmed()
    assert reservation.reservation_status_label == "confirmed"
    reservation.reservation_status_label = "pending"
    with pytest.raises(ReservationExpiredError):
        reservation.mark_expired()


def test_error_subclasses_provide_codes_and_messages() -> None:
    err = InvalidInputError("field", "detail")
    assert "invalid_input" in str(err)
    insurance_error = InsuranceValidationError("pol-1")
    assert insurance_error.error_code == "insurance_invalid"
    gallery_error = GalleryBaseError("code", "message")
    assert str(gallery_error) == "code: message"
    provenance_error = ProvenanceVerificationError("art-1")
    assert "provenance_invalid" in str(provenance_error)


def test_insurance_policy_adjustment_and_logistics_assignment() -> None:
    policy = InsurancePolicy(
        insurance_policy_id="pol-1",
        insurance_artwork_id="art-1",
        insurance_provider_name="Insure",
        insurance_coverage_amount=10_000.0,
        insurance_status_label="pending",
        insurance_expiration_date="2099-01-01",
        insurance_deductible_amount=500.0,
    )
    policy.activate()
    assert policy.adjust_coverage(1000.0) == 11_000.0
    assert policy.mark_expired() == "expired"
    with pytest.raises(InsuranceValidationError):
        policy.adjust_coverage(-20_000.0)
    ticket = LogisticsTicket(
        logistics_ticket_id="log-1",
        logistics_artwork_id="art-1",
        logistics_origin_location="Minsk",
        logistics_destination_location="Paris",
        logistics_scheduled_date="2024-01-01",
        logistics_courier_name="",
        logistics_status_label="scheduled",
    )
    with pytest.raises(LogisticsAssignmentError):
        ticket.validate_assignment()
    ticket.assign_courier("Courier X")
    ticket.validate_assignment()
    ticket.mark_delivered()
    assert ticket.logistics_status_label == "delivered"


def test_account_repository_round_trip_and_filters() -> None:
    repo = InMemoryAccountRepository()
    customer = CustomerProfile(
        customer_id="cust-1",
        customer_email="cust@example.com",
        customer_membership_tier="gold",
        customer_wallet_balance=5000.0,
    )
    visitor = VisitorProfile(
        visitor_id="vis-1",
        visitor_full_name="Visitor",
        visitor_preferred_medium="oil",
    )
    credential = CredentialSecret(
        credential_id="cred-1",
        credential_user_id="cust-1",
        credential_password_hash="hash",
        credential_password_salt="salt",
        credential_failed_attempts=0,
    )
    transaction = TransactionRecord(
        transaction_id="txn-1",
        transaction_artwork_id="art-1",
        transaction_buyer_id="cust-1",
        transaction_amount_value=1000.0,
        transaction_payment_card_id="card-1",
        transaction_status_label="pending",
        transaction_channel_code="web",
    )
    repo.save_customer(customer)
    repo.save_visitor(visitor)
    repo.save_credential(credential)
    repo.save_transaction_record(transaction)
    assert repo.get_customer("cust-1") is customer
    assert repo.get_visitor("vis-1") is visitor
    assert repo.get_credential("cust-1") is credential
    assert repo.list_transactions_for_customer("cust-1")[0] is transaction


def test_dependency_provider_singletons() -> None:
    dependencies.reset_state()
    assert isinstance(dependencies.get_register_customer_use_case(), RegisterCustomerUseCase)
    assert isinstance(dependencies.get_register_visitor_use_case(), RegisterVisitorUseCase)
    assert isinstance(dependencies.get_register_credential_use_case(), RegisterCredentialUseCase)
