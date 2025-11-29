
from typing import List

from src.application.repositories.catalog_repository import CatalogRepository
from src.domain.entities.artwork import Artwork


class ListArtworksUseCase:

    def __init__(self, catalog_repo: CatalogRepository) -> None:
        self._catalog_repo = catalog_repo

    def execute(self) -> List[Artwork]:
        return self._catalog_repo.list_artworks()
