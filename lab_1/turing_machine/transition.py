"""Transition definition for a Turing machine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping

from .enums import Movement


@dataclass(frozen=True)
class Transition:
    """Represents a single transition instruction."""

    next_state: str
    write_symbol: str
    movement: Movement

    def __post_init__(self) -> None:
        if not self.next_state:
            raise ValueError("next_state must be a non-empty string")
        if not isinstance(self.write_symbol, str) or len(self.write_symbol) != 1:
            raise ValueError("write_symbol must be a single character")


class TransitionFunction:
    """Collection of transitions keyed by (state, symbol)."""

    def __init__(self, transitions: Mapping[tuple[str, str], Transition] | None = None) -> None:
        self._table: Dict[tuple[str, str], Transition] = {}
        if transitions:
            for key, transition in transitions.items():
                state, symbol = key
                self.add(state, symbol, transition)

    def add(self, state: str, symbol: str, transition: Transition) -> None:
        if not state:
            raise ValueError("state must be non-empty")
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("symbol must be a single character")
        self._table[(state, symbol)] = transition

    def get(self, state: str, symbol: str) -> Transition | None:
        return self._table.get((state, symbol))

    def states(self) -> Iterable[str]:
        seen: set[str] = set()
        for (state, _), transition in self._table.items():
            seen.add(state)
            seen.add(transition.next_state)
        return tuple(sorted(seen))

    def symbols(self) -> Iterable[str]:
        alphabet = {symbol for _, symbol in self._table}
        alphabet.update(transition.write_symbol for transition in self._table.values())
        return tuple(sorted(alphabet))

    def __repr__(self) -> str:
        parts = ", ".join(
            f"({state!r}, {symbol!r}) -> {transition}"
            for (state, symbol), transition in sorted(self._table.items())
        )
        return f"TransitionFunction({parts})"
