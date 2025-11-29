from src.application.use_cases.authentication.register_credential_use_case import RegisterCredentialUseCase
from src.application.use_cases.authentication.validate_password_use_case import LoginUseCase
from src.application.use_cases.catalog.purchase_artwork_use_case import PurchaseArtworkUseCase
from src.application.use_cases.registration.register_customer_use_case import RegisterCustomerUseCase
from src.application.use_cases.reservations.reserve_artwork_use_case import ReserveArtworkUseCase
from src.domain.entities.artist import Artist
from src.domain.entities.artwork import Artwork
from src.domain.entities.public_exhibition import PublicExhibition
from src.infrastructure.repositories.in_memory_account_repository import InMemoryAccountRepository
from src.infrastructure.repositories.in_memory_catalog_repository import InMemoryCatalogRepository
from src.infrastructure.repositories.in_memory_exhibition_repository import InMemoryExhibitionRepository
from src.infrastructure.repositories.in_memory_reservation_repository import InMemoryReservationRepository
from src.infrastructure.services.identity import SimpleIdentityProvider
from src.infrastructure.services.support import SupportServiceGateway


def build_use_cases():
    catalog_repo = InMemoryCatalogRepository()
    exhibition_repo = InMemoryExhibitionRepository()
    account_repo = InMemoryAccountRepository()
    reservation_repo = InMemoryReservationRepository()
    gateway = SupportServiceGateway()
    identity = SimpleIdentityProvider()

    register_customer_uc = RegisterCustomerUseCase(account_repo, identity)
    register_credential_uc = RegisterCredentialUseCase(account_repo, identity)
    validate_password_uc = LoginUseCase(account_repo)
    purchase_uc = PurchaseArtworkUseCase(
        catalog_repo=catalog_repo,
        account_repo=account_repo,
        payment_gateway=gateway,
        insurance_provider=gateway,
        logistics_provider=gateway,
    )
    reserve_uc = ReserveArtworkUseCase(
        reservation_repo=reservation_repo,
        catalog_repo=catalog_repo,
        logistics_provider=gateway,
    )

    artist = Artist(
        artist_id="artist-usecase",
        artist_stage_name="UC Artist",
        artist_nationality="DE",
        artist_biography_text="Test",
        artist_signature_style="Style",
    )
    catalog_repo.save_artist(artist)
    artwork = Artwork(
        artwork_id="art-usecase",
        artwork_title="Use Case Piece",
        artwork_medium="Ink",
        artwork_creation_year=2020,
        artwork_status_label="available",
        artwork_dimensions_text="30x30",
        artwork_artist_id=artist.artist_id,
        artwork_appraisal_value=2000.0,
    )
    catalog_repo.save_artwork(artwork)
    exhibition = PublicExhibition(
        exhibition_id="exhibit-usecase",
        exhibition_name="Use Case Expo",
        exhibition_location="Hall 1",
        exhibition_capacity=10,
        exhibition_curator_id="curator-1",
        exhibition_private_flag=False,
    )
    exhibition.add_artwork(artwork.artwork_id)
    exhibition_repo.save_exhibition(exhibition)
    return {
        "register_customer": register_customer_uc,
        "register_credential": register_credential_uc,
        "validate_password": validate_password_uc,
        "purchase": purchase_uc,
        "reserve": reserve_uc,
        "account_repo": account_repo,
        "catalog_repo": catalog_repo,
        "reservation_repo": reservation_repo,
        "exhibition_repo": exhibition_repo,
        "gateway": gateway,
    }


def test_registration_and_authentication_flow():
    deps = build_use_cases()
    customer = deps["register_customer"].execute("user@example.com", "silver", 3000.0)
    deps["register_credential"].execute(customer.customer_id, "hash")
    assert deps["account_repo"].get_customer(customer.customer_id).customer_wallet_balance == 3000.0
    deps["validate_password"].execute(customer.customer_id, "hash")


def test_purchase_and_reservation_flow():
    deps = build_use_cases()
    customer = deps["register_customer"].execute("buyer@example.com", "gold", 4000.0)
    deps["register_credential"].execute(customer.customer_id, "hash")
    deps["purchase"].execute(customer.customer_id, "art-usecase", "card-1")
    assert deps["account_repo"].get_customer(customer.customer_id).customer_wallet_balance < 4000.0
    reservation = deps["reserve"].execute(customer.customer_id, "art-usecase", private_view=True)
    assert reservation.reservation_status_label == "pending"
