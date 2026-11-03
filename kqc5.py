import numpy as np

class KumarQuantum:
    def __init__(self, n=2):
        self.n = n
        self.state = np.zeros(2**n, dtype=complex)
        self.state[0] = 1

    def gate(self, matrix, q):
        U = np.array([[1]], dtype=complex)
        for i in range(self.n):
            U = np.kron(U, matrix if i == q else np.eye(2))
        self.state = U @ self.state

    def H(self, q):
        self.gate(np.array([[1,1],[1,-1]])/np.sqrt(2), q)

    def X(self, q):
        self.gate(np.array([[0,1],[1,0]]), q)

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
            for i in range(len(p))
        }

qc = KumarQuantum(2)

print("KQC-5 QUANTUM CIRCUIT")
print("1. H Gate")
print("2. CNOT Gate")

qc.H(0)
qc.CNOT(0, 1)

print("Circuit: H(0) -> CNOT(0,1)")
print("Quantum State:", qc.state)
print("Measurement:", qc.measure(1000))
