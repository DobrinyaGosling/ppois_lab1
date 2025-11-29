import pytest

from turing_machine import (
    ExecutionResult,
    HaltReason,
    MachineSettings,
    MachineSnapshot,
    Movement,
    Tape,
    Transition,
    TransitionFunction,
    TuringMachine,
)


def build_simple_machine() -> TuringMachine:
    transitions = TransitionFunction()
    transitions.add("start", "a", Transition("start", "b", Movement.RIGHT))
    transitions.add("start", "_", Transition("accept", "_", Movement.STAY))
    return TuringMachine.build(
        states=("start", "accept", "reject"),
        blank_symbol="_",
        start_state="start",
        accept_states=("accept",),
        reject_states=("reject",),
        transition_function=transitions,
    )


def test_tape_read_write_and_clone():
    tape = Tape("ab", blank_symbol="_")
    assert tape.read() == "a"
    tape.write("x")
    assert tape.read() == "x"
    tape.move(Movement.RIGHT)
    assert tape.read() == "b"
    snapshot = tape.snapshot(radius=1)
    assert len(snapshot) == 3

    clone = tape.clone()
    clone.move(Movement.LEFT)
    clone.write("c")
    assert tape.read() == "b"  # original unaffected


def test_machine_accepts_and_transforms_input():
    machine = build_simple_machine()
    result = machine.run("aaaa")
    assert isinstance(result, ExecutionResult)
    assert result.accepted
    assert result.halt_reason == HaltReason.ACCEPTED
    assert result.tape.contents() == "bbbb"


def test_machine_rejects_when_transition_missing():
    machine = build_simple_machine()
    tape = machine.initialize_tape("aca")  # 'c' is unknown
    result = machine.run(tape)
    assert result.halt_reason == HaltReason.NO_TRANSITION
    assert result.steps == 1  # fails on first unexpected symbol


def test_step_limit_triggers_expected_reason():
    transitions = TransitionFunction()
    transitions.add("loop", "_", Transition("loop", "_", Movement.STAY))
    machine = TuringMachine.build(
        states=("loop",),
        blank_symbol="_",
        start_state="loop",
        accept_states=(),
        reject_states=(),
        transition_function=transitions,
    )
    result = machine.run("", max_steps=3)
    assert result.halt_reason == HaltReason.STEP_LIMIT_REACHED
    assert result.steps == 3


def test_transition_function_metadata_and_validation():
    transitions = TransitionFunction(
        {("s", "0"): Transition("s", "1", Movement.RIGHT), ("s", "1"): Transition("halt", "1", Movement.STAY)}
    )
    states = transitions.states()
    assert "s" in states and "halt" in states
    assert "0" in transitions.symbols()
    with pytest.raises(ValueError):
        transitions.add("", "0", Transition("s", "0", Movement.RIGHT))
    with pytest.raises(ValueError):
        transitions.add("s", "01", Transition("s", "0", Movement.RIGHT))
    with pytest.raises(ValueError):
        Transition("", "0", Movement.RIGHT)


def test_tape_snapshot_and_iter_cells_behaviour():
    tape = Tape("", blank_symbol="_")
    assert tape.contents() == "_"
    tape.write("a")
    cells = list(tape.iter_cells())
    assert cells == [(0, "a")]
    with pytest.raises(ValueError):
        tape.snapshot(-1)
    with pytest.raises(ValueError):
        tape.write("ab")


def test_machine_settings_validation_rules():
    with pytest.raises(ValueError):
        MachineSettings(states=(), blank_symbol="_", start_state="s", accept_states=(), reject_states=())
    with pytest.raises(ValueError):
        MachineSettings(states=("s",), blank_symbol="_", start_state="x", accept_states=(), reject_states=())
    with pytest.raises(ValueError):
        MachineSettings(states=("s",), blank_symbol="__", start_state="s", accept_states=(), reject_states=())
    with pytest.raises(ValueError):
        MachineSettings(states=("s",), blank_symbol="_", start_state="s", accept_states=("s",), reject_states=("s",))


def test_run_steps_yields_intermediate_snapshots():
    machine = build_simple_machine()
    snapshots = list(machine.run_steps("aa", max_steps=10))
    states = [snapshot.state for snapshot in snapshots]
    assert states[0] == "start"
    assert states[-1] == "accept"
    assert snapshots[-1].steps == len(snapshots) - 1


def test_machine_build_initializes_valid_machine():
    transitions = TransitionFunction()
    transitions.add("start", "_", Transition("accept", "_", Movement.STAY))
    machine = TuringMachine.build(
        states=("start", "accept"),
        blank_symbol="_",
        start_state="start",
        accept_states=("accept",),
        reject_states=(),
        transition_function=transitions,
    )
    tape = machine.initialize_tape("ab")
    assert tape.read() == "a"
    result = machine.run("")
    assert result.halt_reason == HaltReason.ACCEPTED


def test_machine_snapshot_clone_isolated_from_original():
    tape = Tape("a")
    snapshot = MachineSnapshot(state="s", tape=tape)
    clone = snapshot.clone()
    clone.tape.write("b")
    assert snapshot.tape.read() == "a"
