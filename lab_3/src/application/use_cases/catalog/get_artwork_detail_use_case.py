
from src.application.repositories.catalog_repository import CatalogRepository
from src.application.validators import ensure_not_blank
from src.domain.entities.artwork import Artwork
from src.errors import ArtworkNotFoundError


class GetArtworkDetailUseCase:

    def __init__(self, catalog_repo: CatalogRepository) -> None:
        self._catalog_repo = catalog_repo

    def execute(self, artwork_id: str) -> Artwork:
        clean_artwork_id = ensure_not_blank(artwork_id, "artwork_id")
        artwork = self._catalog_repo.get_artwork(clean_artwork_id)
        if artwork is None:
            raise ArtworkNotFoundError(clean_artwork_id)
        return artwork
