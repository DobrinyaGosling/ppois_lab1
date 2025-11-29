from decimal import Decimal

import pytest

from src.domain.entities import Courier, MenuItem, PaymentCard, PromoCode
from src.domain.value_objects import Address, Money


def test_money_operations_and_rounding() -> None:
    price = Money(Decimal("1.235"), "USD")
    multiplied = price.multiply(Decimal("2"))
    assert multiplied.amount == Decimal("2.48")
    discounted = multiplied.subtract(Money(Decimal("0.48"), "USD"))
    assert discounted.amount == Decimal("2.00")


def test_money_currency_mismatch_raises_value_error() -> None:
    dollars = Money(Decimal("5"), "USD")
    euros = Money(Decimal("5"), "EUR")
    with pytest.raises(ValueError):
        _ = dollars.add(euros)


def test_address_label_and_zone_comparison() -> None:
    address = Address("Main", "Minsk", "central")
    same_zone = Address("Side", "Minsk", "central")
    other_zone = Address("Main", "Minsk", "north")
    assert address.label() == "Main, Minsk (central)"
    assert address.same_zone(same_zone)
    assert not address.same_zone(other_zone)


def test_payment_card_charge_and_credit_flow() -> None:
    card = PaymentCard("card-1", "****1234", Money(Decimal("10.00"), "USD"))
    card.charge(Money(Decimal("4.00"), "USD"))
    assert card.balance.amount == Decimal("6.00")
    card.credit(Money(Decimal("2.00"), "USD"))
    assert card.balance.amount == Decimal("8.00")
    card.active = False
    with pytest.raises(ValueError):
        card.charge(Money(Decimal("1.00"), "USD"))


def test_menu_item_adjust_price_and_availability() -> None:
    item = MenuItem("m1", "Soup", Money(Decimal("5.00"), "USD"))
    item.adjust_price(Decimal("1.25"))
    assert item.price.amount == Decimal("6.25")
    item.mark_unavailable()
    assert item.available is False


def test_promo_code_applicability_and_usage_counter() -> None:
    promo = PromoCode("SAVE10", 10, "r1", Money(Decimal("15.00"), "USD"), uses_left=1)
    total = Money(Decimal("30.00"), "USD")
    assert promo.applicable(total, "r1")
    discounted = promo.apply(total)
    assert discounted.amount == Decimal("27.00")
    assert promo.uses_left == 0
    assert promo.applicable(total, "r2") is False


def test_courier_assignment_and_availability() -> None:
    courier = Courier("c1", "Alex", "central", active=True)
    assert courier.is_available()
    courier.assign_order("o1")
    assert courier.is_available() is False
    courier.complete_order()
    assert courier.current_order_id is None
