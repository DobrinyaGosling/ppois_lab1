"""Expose domain-specific exceptions."""

from .artwork_already_sold_error import ArtworkAlreadySoldError
from .artwork_not_found_error import ArtworkNotFoundError
from .curator_not_authorized_error import CuratorNotAuthorizedError
from .customer_not_eligible_error import CustomerNotEligibleForPrivateViewingError
from .exhibition_closed_error import ExhibitionClosedError
from .gallery_base_error import GalleryBaseError
from .insurance_validation_error import InsuranceValidationError
from .invalid_input_error import InvalidInputError
from .insufficient_funds_error import InsufficientFundsError
from .invalid_password_error import InvalidPasswordError
from .logistics_assignment_error import LogisticsAssignmentError
from .payment_authorization_error import PaymentAuthorizationError
from .provenance_verification_error import ProvenanceVerificationError
from .reservation_expired_error import ReservationExpiredError

__all__ = [
    "GalleryBaseError",
    "ArtworkNotFoundError",
    "InvalidPasswordError",
    "ArtworkAlreadySoldError",
    "ExhibitionClosedError",
    "InsufficientFundsError",
    "CustomerNotEligibleForPrivateViewingError",
    "ReservationExpiredError",
    "CuratorNotAuthorizedError",
    "ProvenanceVerificationError",
    "InsuranceValidationError",
    "LogisticsAssignmentError",
    "PaymentAuthorizationError",
    "InvalidInputError",
]
