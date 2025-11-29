from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    street: str
    city: str
    zone: str

    def label(self) -> str:
        return f"{self.street}, {self.city} ({self.zone})"

    def same_zone(self, other: "Address") -> bool:
        return self.zone == other.zone
