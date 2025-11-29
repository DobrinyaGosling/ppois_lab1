"""String parser for Cantor sets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from .cantor_set import CantorElement, CantorSet


@dataclass
class CantorSetParser:
    """Simple recursive-descent parser for Cantor sets."""

    source: str
    factory: Callable[[Iterable["CantorElement"]], "CantorSet"]

    def __post_init__(self) -> None:
        self._index = 0

    def parse(self) -> "CantorSet":
        self._consume_whitespace()
        result = self._parse_set()
        self._consume_whitespace()
        if not self._is_eof():
            raise ValueError("unexpected trailing characters")
        return result

    def _parse_set(self) -> "CantorSet":
        self._expect("{")
        elements: list["CantorElement"] = []
        self._consume_whitespace()
        while not self._match("}"):
            element = self._parse_element()
            elements.append(element)
            self._consume_whitespace()
            if self._match(","):
                self._consume_whitespace()
                continue
            if self._peek() != "}":
                raise ValueError(f"unexpected character at position {self._index}")
        return self.factory(elements)

    def _parse_element(self) -> "CantorElement":
        self._consume_whitespace()
        char = self._peek()
        if char == "{":
            return self._parse_set()
        if char in ("}", ","):
            raise ValueError(f"missing element at position {self._index}")
        return self._parse_token()

    def _parse_token(self) -> str:
        start = self._index
        while not self._is_eof() and self._peek() not in {",", "}"}:
            self._advance()
        token = self.source[start:self._index].strip()
        if not token:
            raise ValueError("empty token detected")
        return token

    def _consume_whitespace(self) -> None:
        while not self._is_eof() and self._peek().isspace():
            self._advance()

    def _peek(self) -> str:
        if self._is_eof():
            raise ValueError("unexpected end of input")
        return self.source[self._index]

    def _match(self, char: str) -> bool:
        if self._is_eof():
            return False
        if self.source[self._index] == char:
            self._advance()
            return True
        return False

    def _expect(self, char: str) -> None:
        if not self._match(char):
            raise ValueError(f"expected '{char}' at position {self._index}")

    def _advance(self) -> None:
        self._index += 1

    def _is_eof(self) -> bool:
        return self._index >= len(self.source)
