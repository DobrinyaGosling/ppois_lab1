
from dataclasses import dataclass

from src.domain.entities.base_exhibition import Exhibition


@dataclass(slots=True)
class PublicExhibition(Exhibition):

    public_ticket_price: float = 0.0
    public_audio_language: str = "en"
    public_guided_tour_slots: int = 0

    def apply_discount(self, fraction: float) -> float:
        self.public_ticket_price *= 1 - fraction
        return self.public_ticket_price

    def assign_language(self, language_code: str) -> str:
        self.public_audio_language = language_code
        return self.public_audio_language

    def schedule_guided_tours(self, slots: int) -> int:
        self.public_guided_tour_slots = max(slots, 0)
        return self.public_guided_tour_slots
