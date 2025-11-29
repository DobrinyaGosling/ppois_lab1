"""Catalog repository interface."""

from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.artist import Artist
from src.domain.entities.artwork import Artwork


class CatalogRepository(ABC):

    @abstractmethod
    def save_artist(self, artist: Artist) -> None: ...

    @abstractmethod
    def save_artwork(self, artwork: Artwork) -> None: ...

    @abstractmethod
    def list_artworks(self) -> List[Artwork]: ...

    @abstractmethod
    def get_artwork(self, artwork_id: str) -> Artwork | None: ...
