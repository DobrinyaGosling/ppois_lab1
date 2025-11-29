
from typing import List

from src.application.repositories.exhibition_repository import ExhibitionRepository
from src.domain.entities.base_exhibition import Exhibition


class ListExhibitionsUseCase:

    def __init__(self, exhibition_repo: ExhibitionRepository) -> None:
        self._exhibition_repo = exhibition_repo

    def execute(self) -> List[Exhibition]:
        return self._exhibition_repo.list_exhibitions()
