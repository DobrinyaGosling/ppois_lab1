from __future__ import annotations

from decimal import Decimal
from typing import Dict, Optional

from src.application.repositories import PromoCodeRepository
from src.domain.entities.promo_code import PromoCode
from src.domain.value_objects.money import Money


class InMemoryPromoCodeRepository(PromoCodeRepository):
    def __init__(self) -> None:
        self.promos: Dict[str, PromoCode] = {
            "HUNGRY10": PromoCode("HUNGRY10", 10, "r1", Money(Decimal("20.00"), "USD"), 5)
        }

    def get(self, code: str) -> Optional[PromoCode]:
        return self.promos.get(code)

    def save(self, promo: PromoCode) -> None:
        self.promos[promo.code] = promo
