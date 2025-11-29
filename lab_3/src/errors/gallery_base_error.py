
from dataclasses import dataclass

@dataclass
class GalleryBaseError(Exception):

    error_code: str
    message: str

    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"
