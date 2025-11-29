"""Exhibition repository interface."""

from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.base_exhibition import Exhibition


class ExhibitionRepository(ABC):

    @abstractmethod
    def list_exhibitions(self) -> List[Exhibition]: ...

    @abstractmethod
    def get_exhibition(self, exhibition_id: str) -> Exhibition | None: ...

    @abstractmethod
    def save_exhibition(self, exhibition: Exhibition) -> None: ...
