from levenshtein_automata.automata import AFN


def test_eclosure():
    automata = AFN((0, 0))
    automata.transitions = {
        (0, 0): {"f": {(1, 0)}, "ANY": {(0, 1), (1, 1)}, "EPSILON": {(1, 1)}},
        (0, 1): {"f": {(1, 1)}},
        (1, 0): {"o": {(2, 0)}, "ANY": {(1, 1), (2, 1)}, "EPSILON": {(2, 1)}},
        (1, 1): {"o": {(2, 1)}},
        (2, 0): {"o": {(3, 0)}, "ANY": {(3, 1), (2, 1)}, "EPSILON": {(3, 1)}},
        (2, 1): {"o": {(3, 1)}},
        (3, 0): {"d": {(4, 0)}, "ANY": {(3, 1), (4, 1)}, "EPSILON": {(4, 1)}},
        (3, 1): {"d": {(4, 1)}},
        (4, 0): {"ANY": {(4, 1)}},
    }
    automata.final_states = {(4, 0), (4, 1)}
    assert automata._eclosure({(0, 0)}) == {(0, 0), (1, 1)}
    assert automata._eclosure({(1, 0)}) == {(1, 0), (2, 1)}
    assert automata._eclosure({(2, 0)}) == {(2, 0), (3, 1)}
    assert automata._eclosure({(3, 0)}) == {(3, 0), (4, 1)}


def test_delta():
    automata = AFN((0, 0))
    automata.transitions = {
        (0, 0): {"f": {(1, 0)}, "ANY": {(0, 1), (1, 1)}, "EPSILON": {(1, 1)}},
        (0, 1): {"f": {(1, 1)}},
        (1, 0): {"o": {(2, 0)}, "ANY": {(1, 1), (2, 1)}, "EPSILON": {(2, 1)}},
        (1, 1): {"o": {(2, 1)}},
        (2, 0): {"o": {(3, 0)}, "ANY": {(3, 1), (2, 1)}, "EPSILON": {(3, 1)}},
        (2, 1): {"o": {(3, 1)}},
        (3, 0): {"d": {(4, 0)}, "ANY": {(3, 1), (4, 1)}, "EPSILON": {(4, 1)}},
        (3, 1): {"d": {(4, 1)}},
        (4, 0): {"ANY": {(4, 1)}},
    }
    automata.final_states = {(4, 0), (4, 1)}

    assert automata._delta("food") == {(3, 1), (4, 0), (4, 1)}
    assert automata._delta("fxod") == {(4, 1)}
