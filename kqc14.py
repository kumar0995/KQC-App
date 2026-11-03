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

circuit = []


def apply_gate(state, gate, q):
    new_state = state.copy()

    for i in range(SIZE):
        if ((i >> q) & 1) == 0:
            j = i | (1 << q)

            a, b = state[i], state[j]

            new_state[i] = gate[0, 0]*a + gate[0, 1]*b
            new_state[j] = gate[1, 0]*a + gate[1, 1]*b

    return new_state


def apply_cnot(state, control, target):
    new_state = state.copy()

    for i in range(SIZE):
        if ((i >> control) & 1) and not ((i >> target) & 1):
            j = i | (1 << target)
            new_state[i] = state[j]
            new_state[j] = state[i]

    return new_state


def add_gate(command):
    if command[0] in GATES and len(command) == 2:
        try:
            q = int(command[1])
            if q not in range(N):
                print("Qubit must be 0 to 7")
                return

            circuit.append([command[0], q])
            print("Gate Added!")

        except ValueError:
            print("Invalid Qubit")

    elif command[0] == "CNOT" and len(command) == 3:
        try:
            c, t = int(command[1]), int(command[2])

            if c not in range(N) or t not in range(N) or c == t:
                print("Choose different qubits from 0 to 7")
                return

            circuit.append(["CNOT", c, t])
            print("CNOT Added!")

        except ValueError:
            print("Invalid Qubit")

    else:
        print("Invalid Command")


def show_diagram():
    print("\n--- KQC-14 CIRCUIT DIAGRAM ---")

    if not circuit:
        print("Circuit is empty!")
        return

    for q in range(N):
        line = f"Q{q} |"

        for gate in circuit:
            if gate[0] == "CNOT":
                if q == gate[1]:
                    line += "--●--"
                elif q == gate[2]:
                    line += "--X--"
                else:
                    line += "-----"

            elif q == gate[1]:
                line += f"--{gate[0]}--"

            else:
                line += "-----"

        print(line)

    print("Total Gates:", len(circuit))


def run_simulation():
    state = np.zeros(SIZE, dtype=complex)
    state[0] = 1

    for gate in circuit:
        if gate[0] in GATES:
            state = apply_gate(state, GATES[gate[0]], gate[1])
        else:
            state = apply_cnot(state, gate[1], gate[2])

    print("\n--- QUANTUM STATE ---")

    for i, amp in enumerate(state):
        if abs(amp) > 1e-8:
            print(f"|{format(i, '08b')}> : {amp}")

    probabilities = np.abs(state)**2
    probabilities /= probabilities.sum()

    results = np.random.choice(SIZE, SHOTS, p=probabilities)

    counts = {}

    for result in results:
        key = format(result, "08b")
        counts[key] = counts.get(key, 0) + 1

    print("\n--- MEASUREMENT RESULTS ---")

    for key, value in sorted(counts.items()):
        print(key, ":", value)

    print("Total Measurements:", SHOTS)


print("\nKUMAR QUANTUM COMPUTER - KQC-14")
print("ADVANCED CIRCUIT ANALYZER")
print("--------------------------------")
print("H 0       - Hadamard")
print("X 0       - X Gate")
print("Y 0       - Y Gate")
print("Z 0       - Z Gate")
print("CNOT 0 1  - CNOT Gate")
print("SHOW      - Circuit Diagram")
print("RUN       - Simulation")
print("CLEAR     - Clear Circuit")
print("EXIT      - Exit")
print("--------------------------------")

while True:
    command = input("KQC-14 > ").upper().split()

    if not command:
        continue

    if command[0] == "EXIT":
        break

    elif command[0] == "SHOW":
        show_diagram()

    elif command[0] == "RUN":
        run_simulation()

    elif command[0] == "CLEAR":
        circuit.clear()
        print("Circuit Cleared!")

    else:
        add_gate(command)

print("\nKQC-14 Closed!")
