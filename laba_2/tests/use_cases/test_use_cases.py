from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from src.application.use_cases import (
    AddItemToCartUseCase,
    ApplyPromoUseCase,
    LoginCustomerUseCase,
    PlaceOrderUseCase,
)
from src.domain.entities.cart import Cart
from src.domain.entities.customer import Customer
from src.domain.entities.line_item import LineItem
from src.domain.entities.menu_item import MenuItem
from src.domain.entities.payment_card import PaymentCard
from src.domain.entities.restaurant import Restaurant
from src.domain.exceptions import CartEmptyError, InvalidPasswordError
from src.domain.value_objects.address import Address
from src.domain.value_objects.money import Money


@pytest.fixture
def sample_customer() -> Customer:
    card = PaymentCard("card", "****", Money(Decimal("50.00"), "USD"))
    return Customer("cust", "Ann", Address("Street", "City", "zone"), "hashed", "salt", 0, [card])


def test_login_customer_invalid_password(sample_customer):
    customers = MagicMock()
    customers.find_by_name.return_value = sample_customer
    use_case = LoginCustomerUseCase(customers)
    with pytest.raises(InvalidPasswordError):
        use_case.execute("Ann", "bad")


def test_add_item_to_cart_use_case(sample_customer):
    cart_repo = MagicMock()
    restaurant_repo = MagicMock()
    cart = Cart("cart-cust", sample_customer.customer_id)
    cart_repo.get_cart.return_value = cart
    menu_item = MenuItem("m1", "Meal", Money(Decimal("11.00"), "USD"))
    restaurant = Restaurant("r1", "Rest", sample_customer.address, [menu_item], 9, 23)
    restaurant_repo.get.return_value = restaurant
    use_case = AddItemToCartUseCase(cart_repo, restaurant_repo)
    result = use_case.execute(sample_customer.customer_id, "r1", "m1", 2)
    assert result.items[0].quantity == 2


def test_apply_promo_use_case_sets_code(sample_customer):
    cart_repo = MagicMock()
    promo_repo = MagicMock()
    restaurant_repo = MagicMock()
    cart = Cart("cart-cust", sample_customer.customer_id)
    cart.add_item(LineItem("m1", "Meal", 1, Money(Decimal("12.00"), "USD")))
    cart_repo.get_cart.return_value = cart
    restaurant_repo.get.return_value = Restaurant("r1", "Rest", sample_customer.address, [], 9, 23)
    promo = MagicMock()
    promo.applicable.return_value = True
    promo_repo.get.return_value = promo
    use_case = ApplyPromoUseCase(cart_repo, promo_repo, restaurant_repo)
    updated = use_case.execute(sample_customer.customer_id, "HUNGRY10", "r1")
    assert updated.promo_code == "HUNGRY10"


def test_place_order_requires_items(sample_customer):
    cart_repo = MagicMock()
    cart_repo.get_cart.return_value = Cart("cart", sample_customer.customer_id)
    order_repo = MagicMock()
    courier_repo = MagicMock()
    customer_repo = MagicMock()
    payment_gateway = MagicMock()
    notification_gateway = MagicMock()
    promo_repo = MagicMock()
    restaurant_repo = MagicMock()
    customer_repo.find_by_id.return_value = sample_customer
    restaurant_repo.get.return_value = Restaurant("r1", "Rest", sample_customer.address, [], 9, 23)
    use_case = PlaceOrderUseCase(
        cart_repo,
        order_repo,
        courier_repo,
        customer_repo,
        payment_gateway,
        notification_gateway,
        promo_repo,
        restaurant_repo,
    )
    with pytest.raises(CartEmptyError):
        use_case.execute(sample_customer.customer_id, "r1")
