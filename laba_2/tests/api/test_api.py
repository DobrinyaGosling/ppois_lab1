from src.presentation.api.routes import cart, customers, orders
from src.presentation.api.schemas import CartItemRequest, CustomerCreateRequest, PlaceOrderRequest

from tests.utils import build_use_case_bundle


def test_register_add_to_cart_and_place_order_via_routes() -> None:
    deps = build_use_case_bundle()
    payload = CustomerCreateRequest(name="Olga", street="Main", city="Minsk", zone="central", password="pass123")
    customer = customers.register_customer(payload, use_case=deps["register"])
    cart_payload = CartItemRequest(
        customer_id=customer.customer_id,
        restaurant_id="r1",
        item_id="m1",
        quantity=2,
    )
    cart.add_cart_item(cart_payload, use_case=deps["add_to_cart"])
    order_payload = PlaceOrderRequest(customer_id=customer.customer_id, restaurant_id="r1", use_loyalty_points=0)
    order = orders.place_order(order_payload, use_case=deps["place_order"])
    assert order.status == "created"


def test_cart_summary_and_cancel_routes() -> None:
    deps = build_use_case_bundle()
    payload = CustomerCreateRequest(name="Nina", street="Main", city="Minsk", zone="central", password="pass123")
    customer = customers.register_customer(payload, use_case=deps["register"])
    cart_payload = CartItemRequest(
        customer_id=customer.customer_id,
        restaurant_id="r2",
        item_id="s1",
        quantity=1,
    )
    cart.add_cart_item(cart_payload, use_case=deps["add_to_cart"])
    summary = cart.summarize_cart(customer.customer_id, use_case=deps["summarize"])
    assert summary["total"] == 18.0
    order_payload = PlaceOrderRequest(customer_id=customer.customer_id, restaurant_id="r2", use_loyalty_points=0)
    order = orders.place_order(order_payload, use_case=deps["place_order"])
    cancelled = orders.cancel_order(order.order_id, use_case=deps["cancel"])
    assert cancelled.status == "cancelled"
