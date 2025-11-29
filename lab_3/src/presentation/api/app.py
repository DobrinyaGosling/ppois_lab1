from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.errors import (
    ArtworkAlreadySoldError,
    ArtworkNotFoundError,
    CuratorNotAuthorizedError,
    CustomerNotEligibleForPrivateViewingError,
    ExhibitionClosedError,
    GalleryBaseError,
    InsufficientFundsError,
    InvalidInputError,
    InvalidPasswordError,
    LogisticsAssignmentError,
    PaymentAuthorizationError,
    ReservationExpiredError,
)
from src.presentation.api.routes import artworks, auth, exhibitions, purchases, reservations, users

app = FastAPI(title="Gallery API")

ERROR_STATUS_MAP = {
    ArtworkNotFoundError: 404,
    InvalidPasswordError: 403,
    InvalidInputError: 400,
    ArtworkAlreadySoldError: 409,
    ExhibitionClosedError: 400,
    InsufficientFundsError: 402,
    CustomerNotEligibleForPrivateViewingError: 403,
    ReservationExpiredError: 410,
    CuratorNotAuthorizedError: 403,
    PaymentAuthorizationError: 402,
    LogisticsAssignmentError: 409,
}


@app.exception_handler(GalleryBaseError)
async def handle_domain_error(_, exc: GalleryBaseError):
    status = ERROR_STATUS_MAP.get(type(exc), 400)
    return JSONResponse(status_code=status, content={"detail": str(exc)})


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(artworks.router)
app.include_router(reservations.router)
app.include_router(exhibitions.router)
app.include_router(purchases.router)
