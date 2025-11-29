"""Machine settings structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class MachineSettings:
    """Immutable description of the machine's allowed states."""

    states: tuple[str, ...]
    blank_symbol: str
    start_state: str
    accept_states: tuple[str, ...]
    reject_states: tuple[str, ...]

    def __init__(
        self,
        states: Sequence[str],
        blank_symbol: str,
        start_state: str,
        accept_states: Iterable[str],
        reject_states: Iterable[str],
    ) -> None:
        object.__setattr__(self, "states", tuple(states))
        object.__setattr__(self, "blank_symbol", blank_symbol)
        object.__setattr__(self, "start_state", start_state)
        object.__setattr__(self, "accept_states", tuple(accept_states))
        object.__setattr__(self, "reject_states", tuple(reject_states))
        self._validate()

    def _validate(self) -> None:
        states = set(self.states)
        if not states:
            raise ValueError("The machine must declare at least one state.")
        if self.start_state not in states:
            raise ValueError("start_state must belong to the provided states.")
        for label, subset in (("accept", self.accept_states), ("reject", self.reject_states)):
            missing = set(subset) - states
            if missing:
                raise ValueError(f"{label} states missing from the state set: {missing}")
        if set(self.accept_states) & set(self.reject_states):
            raise ValueError("accept and reject states must not overlap.")
        if not isinstance(self.blank_symbol, str) or len(self.blank_symbol) != 1:
            raise ValueError("blank_symbol must be a single character.")
