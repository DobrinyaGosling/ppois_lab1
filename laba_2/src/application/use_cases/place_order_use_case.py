from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import secrets

from src.application.gateways import NotificationGateway, PaymentGateway
from src.application.repositories import (
    CartRepository,
    CourierRepository,
    CustomerRepository,
    OrderRepository,
    PromoCodeRepository,
    RestaurantRepository,
)
from src.domain.entities.cart import Cart
from src.domain.entities.order import Order
from src.domain.entities.courier import Courier
from src.exceptions import (
    CartEmptyError,
    CourierUnavailableError,
    CustomerNotFoundError,
    LoyaltyPointsError,
    PromoCodeExpiredError,
    RestaurantClosedError,
)
from src.domain.value_objects.money import Money


@dataclass
class PlaceOrderUseCase:
    cart_repository: CartRepository
    order_repository: OrderRepository
    courier_repository: CourierRepository
    customer_repository: CustomerRepository
    payment_gateway: PaymentGateway
    notification_gateway: NotificationGateway
    promo_repository: PromoCodeRepository
    restaurant_repository: RestaurantRepository

    def execute(self, customer_id: str, restaurant_id: str, use_loyalty_points: int = 0) -> Order:
        customer = self.customer_repository.find_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(customer_id)
        restaurant = self.restaurant_repository.get(restaurant_id)
        if not restaurant or not restaurant.is_open_at(12):
            raise RestaurantClosedError(restaurant_id)
        cart = self.cart_repository.get_cart(customer_id)
        self._ensure_cart_not_empty(cart)
        total = cart.total()
        if cart.promo_code:
            promo = self.promo_repository.get(cart.promo_code)
            if promo and promo.applicable(total, restaurant_id):
                total = promo.apply(total)
                self.promo_repository.save(promo)
            else:
                raise PromoCodeExpiredError(cart.promo_code)
        if use_loyalty_points:
            if use_loyalty_points > customer.loyalty_points:
                raise LoyaltyPointsError(customer_id)
            discount = Money(Decimal(str(use_loyalty_points / 100)), total.currency)
            total = total.subtract(discount)
            customer.redeem_points(use_loyalty_points)
            self.customer_repository.save(customer)
        order = Order(
            order_id=secrets.token_hex(6),
            customer_id=customer_id,
            items=list(cart.items),
            total_amount=total,
            status="created",
            delivery_address=customer.address,
            courier_id=None,
        )
        self.payment_gateway.charge(customer, order)
        courier = self._assign_courier(customer.address.zone)
        order.assign_courier(courier.courier_id)
        courier.assign_order(order.order_id)
        self.courier_repository.save(courier)
        self.order_repository.save(order)
        self.cart_repository.save_cart(Cart(cart_id=cart.cart_id, customer_id=customer_id))
        customer.add_points(int(order.total_amount.amount))
        self.customer_repository.save(customer)
        self.notification_gateway.notify(customer, f"Order {order.order_id} confirmed")
        return order

    def _ensure_cart_not_empty(self, cart: Cart) -> None:
        if not cart.items:
            raise CartEmptyError(cart.cart_id)

    def _assign_courier(self, zone: str) -> Courier:
        available = self.courier_repository.list_availablpayment_gatewaye(zone)
        if not available:
            raise CourierUnavailableError(zone)
        return available[0]
