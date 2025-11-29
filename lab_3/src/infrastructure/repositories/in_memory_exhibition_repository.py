
from typing import Dict, List

from src.application.repositories.exhibition_repository import ExhibitionRepository
from src.domain.entities.base_exhibition import Exhibition


class InMemoryExhibitionRepository(ExhibitionRepository):

    def __init__(self) -> None:
        self.exhibition_storage_map: Dict[str, Exhibition] = {}

    def list_exhibitions(self) -> List[Exhibition]:
        return list(self.exhibition_storage_map.values())

    def get_exhibition(self, exhibition_id: str) -> Exhibition | None:
        return self.exhibition_storage_map.get(exhibition_id)

    def save_exhibition(self, exhibition: Exhibition) -> None:
        self.exhibition_storage_map[exhibition.exhibition_id] = exhibition
