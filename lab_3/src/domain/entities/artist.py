
from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class Artist:

    artist_id: str
    artist_stage_name: str
    artist_nationality: str
    artist_biography_text: str
    artist_signature_style: str
    artist_awards: List[str] = field(default_factory=list)
    artist_artwork_ids: List[str] = field(default_factory=list)

    def add_award(self, award_name: str) -> int:
        if award_name not in self.artist_awards:
            self.artist_awards.append(award_name)
        return len(self.artist_awards)

    def update_biography(self, biography_text: str) -> str:
        self.artist_biography_text = biography_text
        return self.artist_biography_text

    def attach_artwork(self, artwork_id: str) -> int:
        if artwork_id not in self.artist_artwork_ids:
            self.artist_artwork_ids.append(artwork_id)
        return len(self.artist_artwork_ids)
