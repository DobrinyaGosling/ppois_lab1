
from typing import Dict, List

from src.application.repositories.catalog_repository import CatalogRepository
from src.domain.entities.artist import Artist
from src.domain.entities.artwork import Artwork


class InMemoryCatalogRepository(CatalogRepository):

    def __init__(self) -> None:
        self.catalog_storage_artists: Dict[str, Artist] = {}
        self.catalog_storage_artworks: Dict[str, Artwork] = {}

    def save_artist(self, artist: Artist) -> None:
        self.catalog_storage_artists[artist.artist_id] = artist

    def save_artwork(self, artwork: Artwork) -> None:
        self.catalog_storage_artworks[artwork.artwork_id] = artwork

    def list_artworks(self) -> List[Artwork]:
        return list(self.catalog_storage_artworks.values())

    def get_artwork(self, artwork_id: str) -> Artwork | None:
        return self.catalog_storage_artworks.get(artwork_id)
