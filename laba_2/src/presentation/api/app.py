from fastapi import FastAPI

from .routes import auth_router, cart_router, customers_router, orders_router, restaurants_router


def create_app() -> FastAPI:
    app = FastAPI(title="Food Delivery Service")
    app.include_router(customers_router)
    app.include_router(auth_router)
    app.include_router(restaurants_router)
    app.include_router(cart_router)
    app.include_router(orders_router)
    return app


app = create_app()
