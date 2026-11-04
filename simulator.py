import numpy as np

N = 8
SIZE = 2**N
SHOTS = 1000

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

GATES = {
    "H": H,
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex)
}

def run_kqc(circuit):
    state = np.zeros(SIZE, dtype=complex)
    state[0] = 1

    for gate in circuit:
        if gate[0] in GATES:
            new_state = state.copy()
            q = gate[1]

            for i in range(SIZE):
                if ((i >> q) & 1) == 0:
                    j = i | (1 << q)
                    a, b = state[i], state[j]
                    new_state[i] = GATES[gate[0]][0, 0]*a + GATES[gate[0]][0, 1]*b
                    new_state[j] = GATES[gate[0]][1, 0]*a + GATES[gate[0]][1, 1]*b

            state = new_state

        elif gate[0] == "CNOT":
            control, target = gate[1], gate[2]
            new_state = state.copy()

            for i in range(SIZE):
                if ((i >> control) & 1) and not ((i >> target) & 1):
                    j = i | (1 << target)
                    new_state[i] = state[j]
                    new_state[j] = state[i]

            state = new_state

    probabilities = np.abs(state)**2
    probabilities /= probabilities.sum()

    results = np.random.choice(SIZE, SHOTS, p=probabilities)

    counts = {}
    for result in results:
        key = format(result, "08b")
        counts[key] = counts.get(key, 0) + 1

    return state, counts
