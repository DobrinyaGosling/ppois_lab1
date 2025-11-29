from __future__ import annotations

from decimal import Decimal
from typing import Dict, List, Optional

import pytest

from src.application.use_cases import (
    CancelOrderUseCase,
    GetOrderStatusUseCase,
    GetRestaurantMenuUseCase,
    ListRestaurantsUseCase,
    RegisterCustomerUseCase,
    SummarizeCartUseCase,
)
from src.domain.entities import Cart, Customer, LineItem, MenuItem, Order, Restaurant
from src.domain.value_objects import Address, Money
from src.exceptions import OrderAlreadyDeliveredError, OrderNotFoundError, RestaurantClosedError


class StubCustomerRepo:
    def __init__(self) -> None:
        self.saved: List[Customer] = []

    def save(self, customer: Customer) -> None:
        self.saved.append(customer)


class StubNotificationGateway:
    def __init__(self) -> None:
        self.messages: List[str] = []

    def notify(self, customer: Customer, message: str) -> None:
        self.messages.append(f"{customer.customer_id}:{message}")


def test_register_customer_use_case_saves_customer_and_notifies(monkeypatch) -> None:
    repo = StubCustomerRepo()
    gateway = StubNotificationGateway()
    use_case = RegisterCustomerUseCase(repo, gateway)
    tokens = iter(["abcd1234", "face", "customer42"])
    monkeypatch.setattr("src.application.use_cases.register_customer_use_case.secrets.token_hex", lambda _: next(tokens))
    customer = use_case.execute("Ann", "Main", "Minsk", "central", "pwd")
    assert repo.saved[0] is customer
    assert gateway.messages == ["customer42:Welcome to the platform"]
    assert customer.name == "Ann"
    assert customer.cards and customer.cards[0].balance.amount == Decimal("100.00")


class StubCartRepository:
    def __init__(self, cart: Cart) -> None:
        self.cart = cart

    def get_cart(self, customer_id: str) -> Cart:
        assert customer_id == self.cart.customer_id
        return self.cart


def test_summarize_cart_returns_money_total() -> None:
    cart = Cart("cart-1", "cust-1")
    cart.add_item(LineItem("m1", "Meal", 2, Money(Decimal("5.00"), "USD")))
    repo = StubCartRepository(cart)
    use_case = SummarizeCartUseCase(repo)
    total = use_case.execute("cust-1")
    assert total.amount == Decimal("10.00")


class StubRestaurantRepository:
    def __init__(self, restaurants: Dict[str, Restaurant]) -> None:
        self.restaurants = restaurants

    def list_all(self) -> List[Restaurant]:
        return list(self.restaurants.values())

    def get(self, restaurant_id: str) -> Optional[Restaurant]:
        return self.restaurants.get(restaurant_id)


def test_list_restaurants_use_case_delegates_to_repository() -> None:
    repo = StubRestaurantRepository({"r1": Restaurant("r1", "Test", Address("Main", "City", "central"), [], 9, 18)})
    listing = ListRestaurantsUseCase(repo).execute()
    assert listing[0].name == "Test"


def test_get_restaurant_menu_filters_unavailable_items() -> None:
    items = [
        MenuItem("m1", "Ok", Money(Decimal("5.00"), "USD")),
        MenuItem("m2", "Hide", Money(Decimal("4.00"), "USD"), available=False),
    ]
    repo = StubRestaurantRepository({"r1": Restaurant("r1", "Rest", Address("Main", "City", "central"), items, 8, 20)})
    menu = GetRestaurantMenuUseCase(repo).execute("r1")
    assert len(menu) == 1 and menu[0].item_id == "m1"
    with pytest.raises(RestaurantClosedError):
        GetRestaurantMenuUseCase(repo).execute("missing")


class DummyOrderRepository:
    def __init__(self, order: Optional[Order]) -> None:
        self.order = order
        self.saved: List[Order] = []

    def get(self, order_id: str) -> Optional[Order]:
        if self.order and self.order.order_id == order_id:
            return self.order
        return None

    def save(self, order: Order) -> None:
        self.saved.append(order)
        self.order = order


class DummyCourierRepository:
    def __init__(self, courier) -> None:
        self.courier = courier

    def get(self, courier_id: str):
        if self.courier and self.courier.courier_id == courier_id:
            return self.courier
        return None

    def save(self, courier) -> None:
        self.courier = courier


def build_order(status: str = "created", courier_id: str | None = "c1") -> Order:
    return Order(
        order_id="order-1",
        customer_id="cust-1",
        items=[LineItem("m1", "Meal", 1, Money(Decimal("6.00"), "USD"))],
        total_amount=Money(Decimal("6.00"), "USD"),
        status=status,
        delivery_address=Address("Main", "City", "central"),
        courier_id=courier_id,
    )


def test_cancel_order_updates_status_and_courier() -> None:
    from src.domain.entities import Courier

    courier = Courier("c1", "Alex", "central", True, current_order_id="order-1")
    order_repo = DummyOrderRepository(build_order())
    courier_repo = DummyCourierRepository(courier)
    use_case = CancelOrderUseCase(order_repo, courier_repo)
    result = use_case.execute("order-1")
    assert result.status == "cancelled"
    assert courier_repo.get("c1").current_order_id is None
    assert order_repo.saved


def test_cancel_order_missing_or_delivered_raise_errors() -> None:
    use_case = CancelOrderUseCase(DummyOrderRepository(None), DummyCourierRepository(None))
    with pytest.raises(OrderNotFoundError):
        use_case.execute("missing")
    delivered_order = build_order(status="delivered")
    use_case = CancelOrderUseCase(DummyOrderRepository(delivered_order), DummyCourierRepository(None))
    with pytest.raises(OrderAlreadyDeliveredError):
        use_case.execute("order-1")


def test_get_order_status_success_and_missing() -> None:
    order_repo = DummyOrderRepository(build_order(status="preparing"))
    status = GetOrderStatusUseCase(order_repo).execute("order-1")
    assert status == "preparing"
    empty_repo = DummyOrderRepository(None)
    with pytest.raises(OrderNotFoundError):
        GetOrderStatusUseCase(empty_repo).execute("missing")
