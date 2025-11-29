from src.application.interfaces.services import IdentityProviderPort
from src.application.use_cases.authentication.register_credential_use_case import RegisterCredentialUseCase
from src.application.use_cases.authentication.reset_failed_attempts_use_case import ResetFailedAttemptsUseCase
from src.application.use_cases.authentication.validate_password_use_case import LoginUseCase
from src.application.use_cases.catalog.calculate_collection_value_use_case import CalculateCollectionValueUseCase
from src.application.use_cases.catalog.get_artwork_detail_use_case import GetArtworkDetailUseCase
from src.application.use_cases.catalog.get_customer_collection_use_case import GetCustomerCollectionUseCase
from src.application.use_cases.catalog.list_artworks_use_case import ListArtworksUseCase
from src.application.use_cases.catalog.list_exhibitions_use_case import ListExhibitionsUseCase
from src.application.use_cases.catalog.purchase_artwork_use_case import PurchaseArtworkUseCase
from src.application.use_cases.registration.assign_role_to_customer_use_case import AssignRoleToCustomerUseCase
from src.application.use_cases.registration.list_customer_roles_use_case import ListCustomerRolesUseCase
from src.application.use_cases.registration.register_customer_use_case import RegisterCustomerUseCase
from src.application.use_cases.registration.register_visitor_use_case import RegisterVisitorUseCase
from src.application.use_cases.registration.user_registration_use_case import UserRegistrationUseCase
from src.application.use_cases.reservations.cancel_reservation_use_case import CancelReservationUseCase
from src.application.use_cases.reservations.ensure_reservation_validity_use_case import EnsureReservationValidityUseCase
from src.application.use_cases.reservations.list_reservations_use_case import ListReservationsUseCase
from src.application.use_cases.reservations.request_private_access_use_case import RequestPrivateAccessUseCase
from src.application.use_cases.reservations.reserve_artwork_use_case import ReserveArtworkUseCase
from src.domain.entities.artist import Artist
from src.domain.entities.artwork import Artwork
from src.domain.entities.customer import CustomerProfile
from src.domain.entities.public_exhibition import PublicExhibition
from src.domain.entities.visitor import VisitorProfile
from src.infrastructure.repositories.in_memory_account_repository import InMemoryAccountRepository
from src.infrastructure.repositories.in_memory_catalog_repository import InMemoryCatalogRepository
from src.infrastructure.repositories.in_memory_exhibition_repository import InMemoryExhibitionRepository
from src.infrastructure.repositories.in_memory_reservation_repository import InMemoryReservationRepository
from src.infrastructure.services.identity import SimpleIdentityProvider
from src.infrastructure.services.support import SupportServiceGateway

catalog_repository = InMemoryCatalogRepository()
exhibition_repository = InMemoryExhibitionRepository()
account_repository = InMemoryAccountRepository()
reservation_repository = InMemoryReservationRepository()
support_gateway = SupportServiceGateway()
identity_provider: IdentityProviderPort = SimpleIdentityProvider()

_register_customer_use_case = RegisterCustomerUseCase(account_repository, identity_provider)
_register_visitor_use_case = RegisterVisitorUseCase(account_repository, identity_provider)
_assign_role_use_case = AssignRoleToCustomerUseCase(account_repository)
_list_customer_roles_use_case = ListCustomerRolesUseCase(account_repository)
_user_registration_use_case = UserRegistrationUseCase(
    register_customer_use_case=_register_customer_use_case,
    register_visitor_use_case=_register_visitor_use_case,
    register_credential_use_case=RegisterCredentialUseCase(account_repository, identity_provider),
)

_register_credential_use_case = RegisterCredentialUseCase(account_repository, identity_provider)
_validate_password_use_case = LoginUseCase(account_repository)
_reset_failed_attempts_use_case = ResetFailedAttemptsUseCase(account_repository)

_list_artworks_use_case = ListArtworksUseCase(catalog_repository)
_artwork_detail_use_case = GetArtworkDetailUseCase(catalog_repository)
_list_exhibitions_use_case = ListExhibitionsUseCase(exhibition_repository)
_customer_collection_use_case = GetCustomerCollectionUseCase(account_repository)
_collection_value_use_case = CalculateCollectionValueUseCase(account_repository, catalog_repository)
_purchase_artwork_use_case = PurchaseArtworkUseCase(
    catalog_repo=catalog_repository,
    account_repo=account_repository,
    payment_gateway=support_gateway,
    insurance_provider=support_gateway,
    logistics_provider=support_gateway,
)

_reserve_artwork_use_case = ReserveArtworkUseCase(
    reservation_repo=reservation_repository,
    catalog_repo=catalog_repository,
    logistics_provider=support_gateway,
)
_request_private_access_use_case = RequestPrivateAccessUseCase(account_repository, exhibition_repository)
_list_reservations_use_case = ListReservationsUseCase(reservation_repository)
_cancel_reservation_use_case = CancelReservationUseCase(reservation_repository, catalog_repository)
_ensure_reservation_validity_use_case = EnsureReservationValidityUseCase(reservation_repository)


def seed_initial_data() -> None:
    """Populate repositories with initial entries."""
    artist = Artist(
        artist_id="artist-1",
        artist_stage_name="A. Rivera",
        artist_nationality="MX",
        artist_biography_text="Muralist known for bold colors.",
        artist_signature_style="Muralism",
    )
    catalog_repository.save_artist(artist)
    artwork = Artwork(
        artwork_id="artwork-1",
        artwork_title="Sunset Muse",
        artwork_medium="Oil on canvas",
        artwork_creation_year=1950,
        artwork_status_label="available",
        artwork_dimensions_text="80x60",
        artwork_artist_id="artist-1",
        artwork_appraisal_value=5000.0,
    )
    catalog_repository.save_artwork(artwork)
    second_artwork = Artwork(
        artwork_id="artwork-2",
        artwork_title="Marble Dreams",
        artwork_medium="Marble",
        artwork_creation_year=1930,
        artwork_status_label="available",
        artwork_dimensions_text="50x120",
        artwork_artist_id="artist-1",
        artwork_appraisal_value=7000.0,
    )
    catalog_repository.save_artwork(second_artwork)
    exhibition = PublicExhibition(
        exhibition_id="exhibit-1",
        exhibition_name="Modern Echoes",
        exhibition_location="Main Hall",
        exhibition_capacity=100,
        exhibition_curator_id="curator-1",
        exhibition_private_flag=False,
    )
    exhibition.add_artwork("artwork-1")
    exhibition_repository.save_exhibition(exhibition)
    customer = CustomerProfile(
        customer_id="customer-1",
        customer_email="patron@example.com",
        customer_membership_tier="gold",
        customer_wallet_balance=10000.0,
    )
    customer.grant_role("customer")
    account_repository.save_customer(customer)
    visitor = VisitorProfile(
        visitor_id="visitor-1",
        visitor_full_name="Guest Viewer",
        visitor_preferred_medium="sculpture",
    )
    account_repository.save_visitor(visitor)
    _register_credential_use_case.execute("customer-1", "secret")


seed_initial_data()


def reset_state() -> None:
    """Reset in-memory state for testing."""
    catalog_repository.catalog_storage_artists.clear()
    catalog_repository.catalog_storage_artworks.clear()
    exhibition_repository.exhibition_storage_map.clear()
    account_repository.account_storage_customers.clear()
    account_repository.account_storage_visitors.clear()
    account_repository.account_storage_credentials.clear()
    account_repository.account_storage_transactions.clear()
    reservation_repository.reservation_storage_map.clear()
    support_gateway.support_authorizations.clear()
    support_gateway.support_logistics_status.clear()
    support_gateway.support_insurance_policies.clear()
    seed_initial_data()


def get_register_customer_use_case() -> RegisterCustomerUseCase:
    """Dependency provider (used in tests)."""
    return _register_customer_use_case


def get_register_visitor_use_case() -> RegisterVisitorUseCase:
    """Dependency provider (used in tests)."""
    return _register_visitor_use_case


def get_user_registration_use_case() -> UserRegistrationUseCase:
    """High-level user registration use case, used by /users/register."""
    return _user_registration_use_case


def get_assign_role_use_case() -> AssignRoleToCustomerUseCase:
    """Dependency provider."""
    return _assign_role_use_case


def get_list_customer_roles_use_case() -> ListCustomerRolesUseCase:
    """Dependency provider."""
    return _list_customer_roles_use_case


def get_register_credential_use_case() -> RegisterCredentialUseCase:
    """Dependency provider."""
    return _register_credential_use_case


def get_validate_password_use_case() -> LoginUseCase:
    return _validate_password_use_case


def get_reset_failed_attempts_use_case() -> ResetFailedAttemptsUseCase:
    """Dependency provider."""
    return _reset_failed_attempts_use_case


def get_list_artworks_use_case() -> ListArtworksUseCase:
    """Dependency provider."""
    return _list_artworks_use_case


def get_artwork_detail_use_case() -> GetArtworkDetailUseCase:
    """Dependency provider."""
    return _artwork_detail_use_case


def get_list_exhibitions_use_case() -> ListExhibitionsUseCase:
    """Dependency provider."""
    return _list_exhibitions_use_case


def get_customer_collection_use_case() -> GetCustomerCollectionUseCase:
    """Dependency provider."""
    return _customer_collection_use_case


def get_collection_value_use_case() -> CalculateCollectionValueUseCase:
    """Dependency provider."""
    return _collection_value_use_case


def get_purchase_artwork_use_case() -> PurchaseArtworkUseCase:
    """Dependency provider."""
    return _purchase_artwork_use_case


def get_reserve_artwork_use_case() -> ReserveArtworkUseCase:
    """Dependency provider."""
    return _reserve_artwork_use_case


def get_request_private_access_use_case() -> RequestPrivateAccessUseCase:
    """Dependency provider."""
    return _request_private_access_use_case


def get_list_reservations_use_case() -> ListReservationsUseCase:
    """Dependency provider."""
    return _list_reservations_use_case


def get_cancel_reservation_use_case() -> CancelReservationUseCase:
    """Dependency provider."""
    return _cancel_reservation_use_case


def get_ensure_reservation_validity_use_case() -> EnsureReservationValidityUseCase:
    """Dependency provider."""
    return _ensure_reservation_validity_use_case
