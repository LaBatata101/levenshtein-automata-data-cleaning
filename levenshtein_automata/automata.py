from dataclasses import dataclass, field

State = tuple[int, int]
Transition = dict[State, dict[str, set[State]]]


@dataclass
class AFN:
    transitions: Transition = field(init=False, default_factory=lambda: {})
    final_states: set[State] = field(init=False, default_factory=lambda: set())
    start_state: State

    EPSILON = "EPSILON"
    ANY = "ANY"

    def _eclosure(self, states: set[State]):
        dest = set()
        for state in states:
            dest = states.union(self.next_state(state, AFN.EPSILON))

        if states == dest:
            return states

        return self._eclosure(dest)

    def _delta(self, string: str):
        dest_states = self._eclosure({self.start_state})
        for symbol in string:
            for state in dest_states.copy():
                dest_states.remove(state)

                dest_states = dest_states.union(
                    self._eclosure(self.next_state(state, symbol).union(self.next_state(state, AFN.ANY)))
                )

        return dest_states

    def validate_string(self, string: str) -> bool:
        return bool(self.is_final(self._delta(string)))

    def add_transition(self, src: State, symbol: str, dest: State):
        self.transitions.setdefault(src, {}).setdefault(symbol, set()).add(dest)

    def add_final_state(self, state: State):
        self.final_states.add(state)

    def is_final(self, states: set[State]):
        return self.final_states.intersection(states)

    def next_state(self, state, symbol) -> set:
        if state not in self.transitions:
            self.transitions[state] = dict()

        if symbol not in self.transitions[state]:
            self.transitions[state][symbol] = set()

        return self.transitions[state][symbol]
