from src.application.use_cases import (
    AddItemToCartUseCase,
    ApplyPromoUseCase,
    CancelOrderUseCase,
    GetOrderStatusUseCase,
    GetRestaurantMenuUseCase,
    ListRestaurantsUseCase,
    LoginCustomerUseCase,
    PlaceOrderUseCase,
    RegisterCustomerUseCase,
    SummarizeCartUseCase,
)
from . import container


def get_register_customer_use_case() -> RegisterCustomerUseCase:
    return RegisterCustomerUseCase(container.customer_repository, container.notification_gateway)


def get_login_customer_use_case() -> LoginCustomerUseCase:
    return LoginCustomerUseCase(container.customer_repository)


def get_list_restaurants_use_case() -> ListRestaurantsUseCase:
    return ListRestaurantsUseCase(container.restaurant_repository)


def get_menu_use_case() -> GetRestaurantMenuUseCase:
    return GetRestaurantMenuUseCase(container.restaurant_repository)


def get_add_item_to_cart_use_case() -> AddItemToCartUseCase:
    return AddItemToCartUseCase(container.cart_repository, container.restaurant_repository)


def get_summarize_cart_use_case() -> SummarizeCartUseCase:
    return SummarizeCartUseCase(container.cart_repository)


def get_apply_promo_use_case() -> ApplyPromoUseCase:
    return ApplyPromoUseCase(container.cart_repository, container.promo_repository, container.restaurant_repository)


def get_place_order_use_case() -> PlaceOrderUseCase:
    return PlaceOrderUseCase(
        container.cart_repository,
        container.order_repository,
        container.courier_repository,
        container.customer_repository,
        container.payment_gateway,
        container.notification_gateway,
        container.promo_repository,
        container.restaurant_repository,
    )


def get_cancel_order_use_case() -> CancelOrderUseCase:
    return CancelOrderUseCase(container.order_repository, container.courier_repository)


def get_order_status_use_case() -> GetOrderStatusUseCase:
    return GetOrderStatusUseCase(container.order_repository)
