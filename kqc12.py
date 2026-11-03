import numpy as np

N = 8
SHOTS = 1000
SIZE = 2**N

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

GATES = {
    "H": H,
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex)
}

def apply_gate(state, gate, q):
    new_state = state.copy()

    for i in range(SIZE):
        if ((i >> q) & 1) == 0:
            j = i | (1 << q)

            a = state[i]
            b = state[j]

            new_state[i] = gate[0, 0]*a + gate[0, 1]*b
            new_state[j] = gate[1, 0]*a + gate[1, 1]*b

    return new_state


def apply_cnot(state, control, target):
    new_state = state.copy()

    for i in range(SIZE):
        c = (i >> control) & 1
        t = (i >> target) & 1

        if c == 1 and t == 0:
            j = i | (1 << target)
            new_state[i] = state[j]
            new_state[j] = state[i]

    return new_state


def show_state(state):
    print("\n--- QUANTUM STATE ---")

    for i, amplitude in enumerate(state):
        if abs(amplitude) > 1e-8:
            binary = format(i, "08b")
            print(f"|{binary}> : {amplitude}")


def measure(state):
    probabilities = np.abs(state)**2
    probabilities = probabilities / np.sum(probabilities)

    results = np.random.choice(
        SIZE,
        size=SHOTS,
        p=probabilities
    )

    counts = {}

    for result in results:
        binary = format(result, "08b")
        counts[binary] = counts.get(binary, 0) + 1

    print("\n--- MEASUREMENT RESULTS ---")

    for key, value in sorted(counts.items()):
        print(key, ":", value)

    print("\nTotal Measurements:", SHOTS)


def main():
    state = np.zeros(SIZE, dtype=complex)
    state[0] = 1

    print("\nKUMAR QUANTUM COMPUTER - KQC-12")
    print("ADVANCED 8-QUBIT SIMULATOR")
    print("--------------------------------")
    print("Gates: H, X, Y, Z, CNOT")
    print("Qubits: 0 to 7")
    print("Type DONE to run simulation")
    print("--------------------------------")

    gate_count = 0

    while True:
        command = input("KQC-12 > ").upper().split()

        if not command:
            continue

        if command[0] == "DONE":
            break

        if command[0] in GATES and len(command) == 2:
            try:
                q = int(command[1])

                if q not in range(N):
                    print("Qubit must be 0 to 7")
                    continue

                state = apply_gate(state, GATES[command[0]], q)
                gate_count += 1
                print(command[0], "Gate applied to Qubit", q)

            except ValueError:
                print("Invalid qubit number")

        elif command[0] == "CNOT" and len(command) == 3:
            try:
                c, t = int(command[1]), int(command[2])

                if c not in range(N) or t not in range(N) or c == t:
                    print("Choose two different qubits from 0 to 7")
                    continue

                state = apply_cnot(state, c, t)
                gate_count += 1
                print("CNOT applied:", c, "->", t)

            except ValueError:
                print("Invalid qubit number")

        else:
            print("Invalid command")

    print("\nTotal Gates:", gate_count)
    show_state(state)
    measure(state)

    print("\nKQC-12 Simulation Completed!")


main()
