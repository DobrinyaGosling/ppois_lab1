"""Tape implementation for a Turing machine."""

from __future__ import annotations

from typing import Dict, Iterator, Sequence

from .enums import Movement


class Tape:
    """An infinite tape that lazily stores only written cells."""

    def __init__(self, input_data: Sequence[str] | str = "", blank_symbol: str = "_") -> None:
        if not blank_symbol:
            raise ValueError("blank symbol must not be empty")
        if len(blank_symbol) != 1:
            raise ValueError("blank symbol should be a single character")
        self.blank_symbol = blank_symbol
        self._cells: Dict[int, str] = {}
        self._head_position = 0
        symbols = list(input_data) if isinstance(input_data, str) else list(input_data)
        for index, symbol in enumerate(symbols):
            self._validate_symbol(symbol)
            if symbol != self.blank_symbol:
                self._cells[index] = symbol

    @property
    def head_position(self) -> int:
        return self._head_position

    def read(self) -> str:
        """Return the symbol at the current head position."""
        return self._cells.get(self._head_position, self.blank_symbol)

    def write(self, symbol: str) -> None:
        """Write *symbol* to the current head position."""
        self._validate_symbol(symbol)
        if symbol == self.blank_symbol:
            self._cells.pop(self._head_position, None)
        else:
            self._cells[self._head_position] = symbol

    def move(self, movement: Movement) -> None:
        """Move the head according to *movement*."""
        if movement == Movement.LEFT:
            self._head_position -= 1
        elif movement == Movement.RIGHT:
            self._head_position += 1
        elif movement == Movement.STAY:
            return
        else:
            raise ValueError(f"Unsupported movement: {movement!r}")

    def snapshot(self, radius: int = 5) -> str:
        """Return contents around the head, useful for debugging."""
        if radius < 0:
            raise ValueError("radius must be non-negative")
        indexes = range(self._head_position - radius, self._head_position + radius + 1)
        return "".join(self._cells.get(i, self.blank_symbol) for i in indexes)

    def contents(self) -> str:
        """Return the smallest contiguous view that contains all non blank symbols."""
        if not self._cells:
            return self.blank_symbol
        min_index = min(self._cells.keys())
        max_index = max(self._cells.keys())
        return "".join(self._cells.get(i, self.blank_symbol) for i in range(min_index, max_index + 1))

    def clone(self) -> "Tape":
        """Return a deep copy of the tape."""
        clone = Tape("", self.blank_symbol)
        clone._cells = self._cells.copy()
        clone._head_position = self._head_position
        return clone

    def iter_cells(self) -> Iterator[tuple[int, str]]:
        """Yield populated cells in ascending order."""
        for index in sorted(self._cells):
            yield index, self._cells[index]

    def _validate_symbol(self, symbol: str) -> None:
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("symbols must be single characters")

    def __repr__(self) -> str:
        populated = ", ".join(f"{idx}:{sym}" for idx, sym in self.iter_cells())
        return f"Tape(head={self._head_position}, blank={self.blank_symbol!r}, cells={{ {populated} }})"
