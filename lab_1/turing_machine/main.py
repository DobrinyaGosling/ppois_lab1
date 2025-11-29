from turing_machine import TuringMachine, TransitionFunction, Transition, Movement

transitions = TransitionFunction()
transitions.add("start", "a", Transition("start", "b", Movement.RIGHT))
transitions.add("start", "_", Transition("accept", "_", Movement.STAY))
machine = TuringMachine.build(
    states=("start", "accept", "reject"),
    blank_symbol="_",
    start_state="start",
    accept_states=("accept",),
    reject_states=("reject",),
    transition_function=transitions,
)
result = machine.run("aaaa")
print(result.accepted, result.tape.contents())
