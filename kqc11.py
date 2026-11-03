import numpy as np

def deutsch_algorithm():
    print("\n--- DEUTSCH ALGORITHM ---")

    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

    # Two-qubit initial state |01>
    state = np.array([0, 1, 0, 0], dtype=complex)

    state = np.kron(H, H) @ state

    # Balanced oracle
    oracle = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])

    state = oracle @ state
    state = np.kron(H, np.eye(2)) @ state

    probabilities = np.abs(state)**2

    p0 = probabilities[0] + probabilities[1]
    p1 = probabilities[2] + probabilities[3]

    print("Final State:", state)
    print("Probabilities:", probabilities)
    print("First Qubit |0>:", p0)
    print("First Qubit |1>:", p1)
    print("Deutsch Algorithm Completed!")


def grover_search():
    print("\n--- GROVER SEARCH ---")

    n = 4
    target = 2

    state = np.ones(n, dtype=complex) / np.sqrt(n)

    # Oracle
    state[target] *= -1

    # Diffusion
    mean = np.mean(state)
    state = 2 * mean - state

    probabilities = np.abs(state)**2

    print("Target:", target)
    print("Final State:", state)
    print("Probabilities:", probabilities)
    print("Grover Search Completed!")


print("\nKUMAR QUANTUM COMPUTER - KQC-11")
print("1. Deutsch Algorithm")
print("2. Grover Search")
print("3. Run Both")

choice = input("\nChoose Algorithm: ")

if choice == "1":
    deutsch_algorithm()
elif choice == "2":
    grover_search()
elif choice == "3":
    deutsch_algorithm()
    grover_search()
else:
    print("Invalid Choice")

print("\nKQC-11 Completed!")
