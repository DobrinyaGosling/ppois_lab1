from decimal import Decimal

from src.domain import Address, Cart, LineItem, MenuItem, Money, Restaurant


def test_money_operations():
    price = Money(Decimal("10.50"), "USD")
    result = price.add(Money(Decimal("5.00"), "USD"))
    assert result.amount == Decimal("15.50")


def test_cart_total_and_merge():
    cart = Cart(cart_id="c1", customer_id="cust")
    burger = LineItem("b1", "Burger", 1, Money(Decimal("7.00"), "USD"))
    cart.add_item(burger)
    cart.add_item(LineItem("b1", "Burger", 2, Money(Decimal("7.00"), "USD")))
    assert cart.items[0].quantity == 3
    assert cart.total().amount == Decimal("21.00")


def test_restaurant_availability():
    address = Address("Main", "City", "central")
    pizza = MenuItem("p1", "Pizza", Money(Decimal("12.00"), "USD"))
    restaurant = Restaurant("r1", "Test", address, [pizza], 9, 23)
    assert restaurant.is_open_at(12)
    assert restaurant.get_menu_item("p1") == pizza
