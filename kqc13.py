import numpy as np
import json
import os

N = 8
SIZE = 2**N
SHOTS = 1000
FILENAME = "kqc13_circuit.json"

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


def save_circuit():
    with open(FILENAME, "w") as file:
        json.dump(circuit, file, indent=4)

    print("Circuit Saved Successfully!")


def load_circuit():
    global circuit

    if not os.path.exists(FILENAME):
        print("No saved circuit found!")
        return

    try:
        with open(FILENAME, "r") as file:
            loaded = json.load(file)

        for gate in loaded:
            if not isinstance(gate, list):
                raise ValueError

            if gate[0] in GATES and len(gate) == 2:
                if type(gate[1]) != int or gate[1] not in range(N):
                    raise ValueError

            elif gate[0] == "CNOT" and len(gate) == 3:
                c, t = gate[1], gate[2]

                if (type(c) != int or type(t) != int
                        or c not in range(N)
                        or t not in range(N) or c == t):
                    raise ValueError
            else:
                raise ValueError

        circuit = loaded
        print("Circuit Loaded Successfully!")

    except (ValueError, TypeError, json.JSONDecodeError):
        print("Saved circuit file is invalid!")


def show_circuit():
    print("\n--- SAVED CIRCUIT ---")

    if not circuit:
        print("Circuit is empty!")
        return

    for number, gate in enumerate(circuit, 1):
        print(number, ":", gate)


def run_simulation():
    state = np.zeros(SIZE, dtype=complex)
    state[0] = 1

    for gate in circuit:
        if gate[0] in GATES:
            state = apply_gate(state, GATES[gate[0]], gate[1])
        elif gate[0] == "CNOT":
            state = apply_cnot(state, gate[1], gate[2])

    print("\n--- QUANTUM STATE ---")

    for i, amplitude in enumerate(state):
        if abs(amplitude) > 1e-8:
            print(f"|{format(i, '08b')}> :", amplitude)

    probabilities = np.abs(state)**2
    probabilities /= np.sum(probabilities)

    results = np.random.choice(
        SIZE, size=SHOTS, p=probabilities
    )

    counts = {}

    for result in results:
        key = format(result, "08b")
        counts[key] = counts.get(key, 0) + 1

    print("\n--- MEASUREMENT RESULTS ---")

    for key, value in sorted(counts.items()):
        print(key, ":", value)

    print("Total Measurements:", SHOTS)


print("\nKUMAR QUANTUM COMPUTER - KQC-13")
print("QUANTUM CIRCUIT SAVE & LOAD SYSTEM")
print("----------------------------------")
print("H 0       - Hadamard Gate")
print("X 0       - X Gate")
print("Y 0       - Y Gate")
print("Z 0       - Z Gate")
print("CNOT 0 1  - CNOT Gate")
print("SHOW      - Show Circuit")
print("SAVE      - Save Circuit")
print("LOAD      - Load Circuit")
print("RUN       - Run Simulation")
print("CLEAR     - Clear Circuit")
print("EXIT      - Exit Program")
print("----------------------------------")

while True:
    command = input("KQC-13 > ").upper().split()

    if not command:
        continue

    if command[0] == "EXIT":
        break

    elif command[0] == "SHOW":
        show_circuit()

    elif command[0] == "SAVE":
        save_circuit()

    elif command[0] == "LOAD":
        load_circuit()

    elif command[0] == "RUN":
        run_simulation()

    elif command[0] == "CLEAR":
        circuit.clear()
        print("Circuit Cleared!")

    elif command[0] in GATES and len(command) == 2:
        try:
            q = int(command[1])

            if q not in range(N):
                print("Qubit must be 0 to 7")
                continue

            circuit.append([command[0], q])
            print("Gate Added!")

        except ValueError:
            print("Invalid Qubit Number")

    elif command[0] == "CNOT" and len(command) == 3:
        try:
            c, t = int(command[1]), int(command[2])

            if c not in range(N) or t not in range(N) or c == t:
                print("Choose different qubits from 0 to 7")
                continue

            circuit.append(["CNOT", c, t])
            print("CNOT Added!")

        except ValueError:
            print("Invalid Qubit Number")

    else:
        print("Invalid Command!")

print("\nKQC-13 Closed!")
