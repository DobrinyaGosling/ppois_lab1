from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.promo_code import PromoCode


class PromoCodeRepository(ABC):
    @abstractmethod
    def get(self, code: str) -> Optional[PromoCode]:
        raise NotImplementedError

    @abstractmethod
    def save(self, promo: PromoCode) -> None:
        raise NotImplementedError
