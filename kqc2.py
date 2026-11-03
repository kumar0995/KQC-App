import numpy as np

class KQC4:
    def __init__(self):
        self.state = np.zeros(16, dtype=complex)
        self.state[0] = 1

    def gate(self, matrix, qubit):
        gates = [
            matrix if i == qubit else np.eye(2)
            for i in range(4)
        ]

        U = np.array([[1]], dtype=complex)

        for g in gates:
            U = np.kron(U, g)

        self.state = U @ self.state

    def H(self, qubit):
        H = np.array([
            [1, 1],
            [1, -1]
        ]) / np.sqrt(2)

        self.gate(H, qubit)

    def X(self, qubit):
        X = np.array([
            [0, 1],
            [1, 0]
        ])

        self.gate(X, qubit)

    def Z(self, qubit):
        Z = np.array([
            [1, 0],
            [0, -1]
        ])

        self.gate(Z, qubit)

    def CNOT(self, control, target):
        new_state = np.zeros(16, dtype=complex)

        for i, amp in enumerate(self.state):
            bits = list(format(i, '04b'))

            if bits[control] == '1':
                bits[target] = '1' if bits[target] == '0' else '0'

            j = int(''.join(bits), 2)
            new_state[j] += amp

        self.state = new_state

    def measure(self, shots=1000):
        p = np.abs(self.state) ** 2
        results = np.random.choice(16, shots, p=p)

        return {
            format(i, '04b'): int(np.sum(results == i))
            for i in range(16)
        }

qc = KQC4()

qc.H(0)
qc.CNOT(0, 1)
qc.CNOT(0, 2)
qc.CNOT(0, 3)

print("KUMAR QUANTUM COMPUTER - KQC-4")
print("FOUR QUBIT GHZ ENTANGLEMENT")
print("Quantum State:", qc.state)
print("Measurement:", qc.measure(1000))
