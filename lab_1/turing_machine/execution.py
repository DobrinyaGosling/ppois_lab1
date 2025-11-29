"""Execution result models for the Turing machine."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import HaltReason
from .tape import Tape


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Represents the outcome of a machine run."""

    final_state: str
    halt_reason: HaltReason
    steps: int
    tape: Tape

    @property
    def accepted(self) -> bool:
        return self.halt_reason == HaltReason.ACCEPTED
