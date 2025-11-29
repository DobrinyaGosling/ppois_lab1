from decimal import Decimal

import pytest

from src.domain.entities import Cart, Customer, LineItem, Order, PaymentCard
from src.domain.value_objects import Address, Money
from src.infrastructure.gateways import InMemoryPaymentGateway, SimpleNotificationGateway
from src.infrastructure.repositories import (
    InMemoryCartRepository,
    InMemoryCourierRepository,
    InMemoryCustomerRepository,
    InMemoryOrderRepository,
    InMemoryPromoCodeRepository,
    InMemoryRestaurantRepository,
)
from src.exceptions import InsufficientFundsError


def _sample_address() -> Address:
    return Address("Main", "Minsk", "central")


def test_cart_repository_returns_same_instance_for_customer() -> None:
    repo = InMemoryCartRepository()
    cart_a = repo.get_cart("cust-1")
    cart_a.add_item(LineItem("m1", "Meal", 1, Money(Decimal("5.00"), "USD")))
    repo.save_cart(cart_a)
    cart_b = repo.get_cart("cust-1")
    assert cart_a is cart_b
    assert cart_b.total().amount == Decimal("5.00")


def test_customer_repository_supports_lookup_by_name_and_id() -> None:
    repo = InMemoryCustomerRepository()
    customer = Customer("cust-1", "Ann", _sample_address(), "hash", "salt", 0, [])
    repo.save(customer)
    assert repo.find_by_id("cust-1") is customer
    assert repo.find_by_name("Ann") is customer
    assert repo.find_by_name("Unknown") is None


def test_order_repository_filters_orders_by_customer() -> None:
    repo = InMemoryOrderRepository()
    order = Order(
        order_id="o1",
        customer_id="cust-1",
        items=[LineItem("m1", "Meal", 1, Money(Decimal("9.00"), "USD"))],
        total_amount=Money(Decimal("9.00"), "USD"),
        status="created",
        delivery_address=_sample_address(),
        courier_id=None,
    )
    repo.save(order)
    assert repo.get("o1") is order
    assert repo.list_for_customer("cust-1") == [order]
    assert repo.list_for_customer("cust-2") == []


def test_restaurant_repository_lists_all_and_menus() -> None:
    repo = InMemoryRestaurantRepository()
    restaurants = repo.list_all()
    assert len(restaurants) >= 2
    menu = repo.list_menu("r1")
    assert menu
    assert repo.get("missing") is None


def test_promo_repository_updates_stored_promotions() -> None:
    repo = InMemoryPromoCodeRepository()
    promo = repo.get("HUNGRY10")
    assert promo is not None
    promo.uses_left = 0
    repo.save(promo)
    assert repo.get("HUNGRY10").uses_left == 0


def test_courier_repository_filters_by_zone_and_updates_state() -> None:
    repo = InMemoryCourierRepository()
    available = repo.list_available("central")
    assert available
    courier = available[0]
    courier.assign_order("order-1")
    repo.save(courier)
    assert repo.list_available("central") == []
    assert repo.get(courier.courier_id).current_order_id == "order-1"


def test_payment_gateway_charge_and_loyalty_behaviour() -> None:
    gateway = InMemoryPaymentGateway()
    card = PaymentCard("card-1", "****", Money(Decimal("20.00"), "USD"))
    customer = Customer("cust-1", "Ann", _sample_address(), "hash", "salt", 0, [card])
    order = Order(
        order_id="o1",
        customer_id="cust-1",
        items=[],
        total_amount=Money(Decimal("5.00"), "USD"),
        status="created",
        delivery_address=_sample_address(),
        courier_id=None,
    )
    gateway.charge(customer, order)
    assert customer.cards[0].balance.amount == Decimal("15.00")
    gateway.apply_loyalty(customer, 10)
    assert customer.loyalty_points == 10
    customer.cards.clear()
    with pytest.raises(InsufficientFundsError):
        gateway.charge(customer, order)


def test_notification_gateway_stores_messages() -> None:
    gateway = SimpleNotificationGateway()
    customer = Customer("cust-2", "Oleg", _sample_address(), "hash", "salt", 0, [])
    gateway.notify(customer, "Hello")
    assert gateway.sent_messages == ["cust-2:Hello"]
