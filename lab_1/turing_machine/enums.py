"""Shared enumerations for the Turing machine implementation."""

from __future__ import annotations

from enum import Enum


class Movement(str, Enum):
    """Represents a tape head movement."""

    LEFT = "L"
    RIGHT = "R"
    STAY = "S"


class HaltReason(str, Enum):
    """Describes the reason why a machine execution stopped."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NO_TRANSITION = "no_transition"
    STEP_LIMIT_REACHED = "step_limit_reached"
