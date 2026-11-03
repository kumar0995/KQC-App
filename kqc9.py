import numpy as np

class KumarQuantum:
    def __init__(self, n=8):
        self.n = n
        self.state = np.zeros(2**n, dtype=complex)
        self.state[0] = 1

    def gate(self, matrix, q):
        U = np.array([[1]], dtype=complex)
        for i in range(self.n):
            U = np.kron(U, matrix if i == q else np.eye(2))
        self.state = U @ self.state

    def H(self, q):
        self.gate(np.array([[1, 1], [1, -1]]) / np.sqrt(2), q)

    def X(self, q):
        self.gate(np.array([[0, 1], [1, 0]]), q)

    def Y(self, q):
        self.gate(np.array([[0, -1j], [1j, 0]]), q)

    def Z(self, q):
        self.gate(np.array([[1, 0], [0, -1]]), q)

    def CNOT(self, c, t):
        new = np.zeros_like(self.state)
        for i, amp in enumerate(self.state):
            bits = list(format(i, f'0{self.n}b'))
            if bits[c] == '1':
                bits[t] = '1' if bits[t] == '0' else '0'
            new[int(''.join(bits), 2)] += amp
        self.state = new

    def measure(self, shots=1000):
        p = np.abs(self.state)**2
        r = np.random.choice(len(p), shots, p=p)
        return {
            format(i, f'0{self.n}b'): int(np.sum(r == i))
            for i in range(len(p)) if np.sum(r == i) > 0
        }

qc = KumarQuantum(8)

print("\nKUMAR QUANTUM COMPUTER - KQC-9")
print("Qubits: 0 to 7")
print("Gates: H, X, Y, Z, CNOT")
print("Example: H 0")
print("Example: CNOT 0 1")
print("Type DONE to finish\n")

while True:
    command = input("KQC-9 > ").upper().split()

    if not command:
        continue

    if command[0] == "DONE":
        break

    try:
        if command[0] in ["H", "X", "Y", "Z"] and len(command) == 2:
            q = int(command[1])
            if q not in range(8):
                print("Qubit must be 0 to 7")
                continue
            getattr(qc, command[0])(q)
            print("Gate added!")

        elif command[0] == "CNOT" and len(command) == 3:
            c, t = int(command[1]), int(command[2])
            if c not in range(8) or t not in range(8) or c == t:
                print("Choose two different qubits")
                continue
            qc.CNOT(c, t)
            print("CNOT added!")

        else:
            print("Invalid command")

    except ValueError:
        print("Enter valid numbers")

print("\nKQC-9 Circuit Completed!")
print("Quantum State:", qc.state)
print("Measurement:", qc.measure(1000))
