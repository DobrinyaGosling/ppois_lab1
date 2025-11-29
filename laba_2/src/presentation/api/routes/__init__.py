from .customers import router as customers_router
from .auth import router as auth_router
from .restaurants import router as restaurants_router
from .cart import router as cart_router
from .orders import router as orders_router

__all__ = [
    "customers_router",
    "auth_router",
    "restaurants_router",
    "cart_router",
    "orders_router",
]
