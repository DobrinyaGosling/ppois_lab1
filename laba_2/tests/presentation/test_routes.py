from src.presentation.api.routes import cart, customers, orders
from src.presentation.api.schemas import CartItemRequest, CustomerCreateRequest, PlaceOrderRequest

from tests.utils import build_use_case_bundle


def test_route_flow_register_cart_order_status_cancel() -> None:
    deps = build_use_case_bundle()
    customer_payload = CustomerCreateRequest(name="Lena", street="Main", city="Minsk", zone="central", password="secret")
    customer_response = customers.register_customer(customer_payload, use_case=deps["register"])
    cart_payload = CartItemRequest(
        customer_id=customer_response.customer_id,
        restaurant_id="r1",
        item_id="m1",
        quantity=2,
    )
    cart_result = cart.add_cart_item(cart_payload, use_case=deps["add_to_cart"])
    assert cart_result["total"] == 24.0
    order_payload = PlaceOrderRequest(
        customer_id=customer_response.customer_id,
        restaurant_id="r1",
        use_loyalty_points=0,
    )
    order_response = orders.place_order(order_payload, use_case=deps["place_order"])
    assert order_response.status == "created"
    status = orders.order_status(order_response.order_id, use_case=deps["status"])
    assert status["status"] == "created"
    cancelled = orders.cancel_order(order_response.order_id, use_case=deps["cancel"])
    assert cancelled.status == "cancelled"


def test_cart_summary_route_returns_numeric_total() -> None:
    deps = build_use_case_bundle()
    customer_payload = CustomerCreateRequest(name="Ivan", street="Main", city="Minsk", zone="central", password="secret")
    response = customers.register_customer(customer_payload, use_case=deps["register"])
    cart_payload = CartItemRequest(
        customer_id=response.customer_id,
        restaurant_id="r2",
        item_id="s1",
        quantity=1,
    )
    cart.add_cart_item(cart_payload, use_case=deps["add_to_cart"])
    summary = cart.summarize_cart(response.customer_id, use_case=deps["summarize"])
    assert summary["total"] == 18.0


def test_apply_promo_route_updates_cart_code() -> None:
    deps = build_use_case_bundle()
    customer_payload = CustomerCreateRequest(name="Maya", street="Main", city="Minsk", zone="central", password="secret")
    customer = customers.register_customer(customer_payload, use_case=deps["register"])
    cart_payload = CartItemRequest(
        customer_id=customer.customer_id,
        restaurant_id="r1",
        item_id="m1",
        quantity=2,
    )
    cart.add_cart_item(cart_payload, use_case=deps["add_to_cart"])
    response = cart.apply_promo(
        customer_id=customer.customer_id,
        restaurant_id="r1",
        promo_code="HUNGRY10",
        use_case=deps["apply_promo"],
    )
    assert response["promo_code"] == "HUNGRY10"
