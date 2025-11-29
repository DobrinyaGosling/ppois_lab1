from src.infrastructure.repositories import (
    InMemoryCartRepository,
    InMemoryCourierRepository,
    InMemoryCustomerRepository,
    InMemoryOrderRepository,
    InMemoryPromoCodeRepository,
    InMemoryRestaurantRepository,
)
from src.infrastructure.gateways import InMemoryPaymentGateway, SimpleNotificationGateway

customer_repository = InMemoryCustomerRepository()
restaurant_repository = InMemoryRestaurantRepository()
cart_repository = InMemoryCartRepository()
order_repository = InMemoryOrderRepository()
courier_repository = InMemoryCourierRepository()
promo_repository = InMemoryPromoCodeRepository()
payment_gateway = InMemoryPaymentGateway()
notification_gateway = SimpleNotificationGateway()
