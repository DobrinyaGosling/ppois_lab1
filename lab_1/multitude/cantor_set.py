"""Implementation of an unordered Cantor set with parsing support."""

from __future__ import annotations

from typing import Iterable, Iterator


class CantorSet:
    """Immutable recursive set structure."""

    def __init__(self, elements: Iterable["CantorElement"] | None = None) -> None:
        normalized = {self._normalize(element) for element in elements or ()}
        self._elements = frozenset(normalized)

    @classmethod
    def from_string(cls, source: str) -> "CantorSet":
        from .parser import CantorSetParser

        parser = CantorSetParser(source=source, factory=cls)
        return parser.parse()

    def with_element(self, element: "CantorElement") -> "CantorSet":
        normalized = self._normalize(element)
        return CantorSet(self._elements | {normalized})

    def union(self, other: "CantorSet") -> "CantorSet":
        self._ensure_set(other)
        return CantorSet(self._elements | other._elements)

    def intersection(self, other: "CantorSet") -> "CantorSet":
        self._ensure_set(other)
        return CantorSet(self._elements & other._elements)

    def difference(self, other: "CantorSet") -> "CantorSet":
        self._ensure_set(other)
        return CantorSet(self._elements - other._elements)

    def is_subset_of(self, other: "CantorSet") -> bool:
        self._ensure_set(other)
        return self._elements.issubset(other._elements)

    def flatten(self) -> set[str]:
        result: set[str] = set()
        for element in self._elements:
            if isinstance(element, CantorSet):
                result.update(element.flatten())
            else:
                result.add(element)
        return result

    def __contains__(self, element: object) -> bool:
        if isinstance(element, CantorSet):
            return element in self._elements
        if isinstance(element, str):
            normalized = element.strip()
            if not normalized:
                return False
            return normalized in self._elements
        return False

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self) -> Iterator["CantorElement"]:
        yield from self._elements

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CantorSet):
            return NotImplemented
        return self._elements == other._elements

    def __hash__(self) -> int:
        return hash(self._elements)

    def __repr__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        parts = []
        for element in sorted(self._elements, key=self._string_key):
            if isinstance(element, CantorSet):
                parts.append(element.to_string())
            else:
                parts.append(element)
        return "{" + ", ".join(parts) + "}"

    def _ensure_set(self, other: "CantorSet") -> None:
        if not isinstance(other, CantorSet):
            raise TypeError("argument must be a CantorSet")

    def _normalize(self, element: "CantorElement") -> "CantorElement":
        if isinstance(element, CantorSet):
            return element
        if isinstance(element, str):
            stripped = element.strip()
            if not stripped:
                raise ValueError("empty strings are not valid elements")
            return stripped
        raise TypeError("elements must be strings or CantorSet instances")

    def _string_key(self, element: "CantorElement"):
        if isinstance(element, CantorSet):
            return (1, element.to_string())
        return (0, element)


CantorElement = str | CantorSet
