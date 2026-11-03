gates = []

print("\nKUMAR QUANTUM COMPUTER - KQC-10")
print("QUANTUM CIRCUIT VISUALIZER")
print("Available: H, X, Y, Z, CNOT")
print("Qubit: 0 to 7")
print("Type DONE to finish\n")

while True:
    command = input("KQC-10 > ").upper().split()

    if not command:
        continue

    if command[0] == "DONE":
        break

    if command[0] in ["H", "X", "Y", "Z"] and len(command) == 2:
        try:
            q = int(command[1])
            if q not in range(8):
                print("Qubit must be 0 to 7")
                continue
            gates.append((command[0], q))
            print("Gate added!")
        except ValueError:
            print("Invalid qubit number")

    elif command[0] == "CNOT" and len(command) == 3:
        try:
            c, t = int(command[1]), int(command[2])
            if c not in range(8) or t not in range(8) or c == t:
                print("Choose two different qubits from 0 to 7")
                continue
            gates.append(("CNOT", c, t))
            print("CNOT added!")
        except ValueError:
            print("Invalid qubit number")

    else:
        print("Invalid command")

print("\nKQC-10 CIRCUIT DIAGRAM")
print("======================")

for q in range(8):
    line = f"Q{q} |"
    for gate in gates:
        if gate[0] == "CNOT":
            if q == gate[1]:
                line += "---●---"
            elif q == gate[2]:
                line += "---X---"
            else:
                line += "-------"
        elif q == gate[1]:
            line += f"--{gate[0]}--"
        else:
            line += "------"
    print(line)

print("\nTotal Gates:", len(gates))
print("KQC-10 Visualization Completed!")
