from __future__ import annotations

from src.application.use_cases import (
    AddItemToCartUseCase,
    ApplyPromoUseCase,
    CancelOrderUseCase,
    GetOrderStatusUseCase,
    PlaceOrderUseCase,
    RegisterCustomerUseCase,
    SummarizeCartUseCase,
)
from src.infrastructure.gateways import InMemoryPaymentGateway, SimpleNotificationGateway
from src.infrastructure.repositories import (
    InMemoryCartRepository,
    InMemoryCourierRepository,
    InMemoryCustomerRepository,
    InMemoryOrderRepository,
    InMemoryPromoCodeRepository,
    InMemoryRestaurantRepository,
)


def build_use_case_bundle() -> dict[str, object]:
    customer_repo = InMemoryCustomerRepository()
    restaurant_repo = InMemoryRestaurantRepository()
    cart_repo = InMemoryCartRepository()
    order_repo = InMemoryOrderRepository()
    courier_repo = InMemoryCourierRepository()
    promo_repo = InMemoryPromoCodeRepository()
    payment_gateway = InMemoryPaymentGateway()
    notification_gateway = SimpleNotificationGateway()
    return {
        "register": RegisterCustomerUseCase(customer_repo, notification_gateway),
        "add_to_cart": AddItemToCartUseCase(cart_repo, restaurant_repo),
        "summarize": SummarizeCartUseCase(cart_repo),
        "apply_promo": ApplyPromoUseCase(cart_repo, promo_repo, restaurant_repo),
        "place_order": PlaceOrderUseCase(
            cart_repo,
            order_repo,
            courier_repo,
            customer_repo,
            payment_gateway,
            notification_gateway,
            promo_repo,
            restaurant_repo,
        ),
        "cancel": CancelOrderUseCase(order_repo, courier_repo),
        "status": GetOrderStatusUseCase(order_repo),
    }
