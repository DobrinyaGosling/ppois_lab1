"""Core machine runtime logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence

from .enums import HaltReason
from .execution import ExecutionResult
from .settings import MachineSettings
from .tape import Tape
from .transition import Transition, TransitionFunction


@dataclass(slots=True)
class MachineSnapshot:
    """Represents the machine at a specific moment."""

    state: str
    tape: Tape
    steps: int = 0

    def clone(self) -> "MachineSnapshot":
        return MachineSnapshot(state=self.state, tape=self.tape.clone(), steps=self.steps)


class TuringMachine:
    """Deterministic single-tape Turing machine."""

    def __init__(self, settings: MachineSettings, transition_function: TransitionFunction) -> None:
        self.settings = settings
        self.transition_function = transition_function

    @classmethod
    def build(
        cls,
        states: Sequence[str],
        blank_symbol: str,
        start_state: str,
        accept_states: Iterable[str],
        reject_states: Iterable[str],
        transition_function: TransitionFunction,
    ) -> "TuringMachine":
        settings = MachineSettings(
            states=states,
            blank_symbol=blank_symbol,
            start_state=start_state,
            accept_states=accept_states,
            reject_states=reject_states,
        )
        return cls(settings=settings, transition_function=transition_function)

    def initialize_tape(self, input_data: Sequence[str] | str = "") -> Tape:
        """Return a new tape preloaded with *input_data*."""
        return Tape(input_data, blank_symbol=self.settings.blank_symbol)

    def run(
        self,
        input_data: Sequence[str] | str | Tape = "",
        max_steps: int | None = 10_000,
    ) -> ExecutionResult:
        snapshot = self._bootstrap_snapshot(input_data)
        halt_reason = self._execute(snapshot, max_steps)
        return ExecutionResult(
            final_state=snapshot.state,
            halt_reason=halt_reason,
            steps=snapshot.steps,
            tape=snapshot.tape,
        )

    def run_steps(
        self,
        input_data: Sequence[str] | str | Tape = "",
        max_steps: int | None = 10_000,
    ) -> Iterator[MachineSnapshot]:
        """Yield snapshots after each step for debugging/visualization."""
        snapshot = self._bootstrap_snapshot(input_data)
        yield snapshot.clone()

        reason = self._halt_reason(snapshot, max_steps)
        if reason is not None:
            return

        while True:
            transition = self._next_transition(snapshot)
            if transition is None:
                return
            self._apply_transition(snapshot, transition)
            yield snapshot.clone()
            reason = self._halt_reason(snapshot, max_steps)
            if reason is not None:
                return

    def _bootstrap_snapshot(self, input_data: Sequence[str] | str | Tape) -> MachineSnapshot:
        tape = input_data.clone() if isinstance(input_data, Tape) else self.initialize_tape(input_data)
        return MachineSnapshot(state=self.settings.start_state, tape=tape)

    def _execute(self, snapshot: MachineSnapshot, max_steps: int | None) -> HaltReason:
        reason = self._halt_reason(snapshot, max_steps)
        if reason is not None:
            return reason

        while True:
            transition = self._next_transition(snapshot)
            if transition is None:
                return HaltReason.NO_TRANSITION
            self._apply_transition(snapshot, transition)
            reason = self._halt_reason(snapshot, max_steps)
            if reason is not None:
                return reason

    def _halt_reason(self, snapshot: MachineSnapshot, max_steps: int | None) -> HaltReason | None:
        state = snapshot.state
        if state in self.settings.accept_states:
            return HaltReason.ACCEPTED
        if state in self.settings.reject_states:
            return HaltReason.REJECTED
        if max_steps is not None and snapshot.steps >= max_steps:
            return HaltReason.STEP_LIMIT_REACHED
        return None

    def _next_transition(self, snapshot: MachineSnapshot) -> Transition | None:
        symbol = snapshot.tape.read()
        return self.transition_function.get(snapshot.state, symbol)

    def _apply_transition(self, snapshot: MachineSnapshot, transition: Transition) -> None:
        snapshot.tape.write(transition.write_symbol)
        snapshot.tape.move(transition.movement)
        snapshot.state = transition.next_state
        snapshot.steps += 1
