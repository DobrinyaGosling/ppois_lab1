
from dataclasses import dataclass, field
from typing import List

from src.errors import ExhibitionClosedError


@dataclass(slots=True)
class Exhibition:

    exhibition_id: str  #выставки
    exhibition_name: str
    exhibition_location: str
    exhibition_capacity: int
    exhibition_curator_id: str
    exhibition_private_flag: bool
    exhibition_artwork_ids: List[str] = field(default_factory=list)
    exhibition_attendance_count: int = 0

    def add_artwork(self, artwork_id: str) -> int:
        if artwork_id not in self.exhibition_artwork_ids:
            self.exhibition_artwork_ids.append(artwork_id)
        return len(self.exhibition_artwork_ids)

    def record_visit(self) -> int:
        if self.is_full():
            raise ExhibitionClosedError(self.exhibition_id)
        self.exhibition_attendance_count += 1
        return self.exhibition_attendance_count

    def is_full(self) -> bool:
        return self.exhibition_attendance_count >= self.exhibition_capacity

    def open_to_public(self) -> None:
        self.exhibition_attendance_count = 0
