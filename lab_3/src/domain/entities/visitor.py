
from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class VisitorProfile:

    visitor_id: str
    visitor_full_name: str
    visitor_preferred_medium: str
    visitor_feedback_notes: List[str] = field(default_factory=list)
    visitor_loyalty_points: int = 0
    visitor_reservation_ids: List[str] = field(default_factory=list)

    def add_feedback(self, note: str) -> int:
        """Record visitor feedback."""
        self.visitor_feedback_notes.append(note)
        return len(self.visitor_feedback_notes)

    def add_reservation(self, reservation_id: str) -> int:
        """Append reservation id."""
        self.visitor_reservation_ids.append(reservation_id)
        return len(self.visitor_reservation_ids)

    def redeem_points(self, points: int) -> int:
        """Redeem loyalty points."""
        self.visitor_loyalty_points = max(self.visitor_loyalty_points - points, 0)
        return self.visitor_loyalty_points
