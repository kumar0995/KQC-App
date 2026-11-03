from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create our first quantum circuit
qc = QuantumCircuit(1, 1)

# Put qubit into superposition
qc.h(0)

# Measure qubit
qc.measure(0, 0)

# Run simulation
simulator = AerSimulator()
job = simulator.run(qc, shots=1000)
result = job.result()

print("Kumar Quantum Computer - KQC-1")
print(result.get_counts())python kqc1.py
Kumar Quantum Computer - KQC-1{'0': 503, '1': 497}
pkg install python numpy scipy matplotlib -y
pkg install python numpy scipy matplotlib -y
+
