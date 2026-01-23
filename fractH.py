from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.circuit.library import RYGate
from qiskit.circuit.library import RZGate
import os

import matplotlib.pyplot as plt  
import math

def psi_angles(M, t):
    ang = []
    for i in range(M-2, -1, -1):
        if i == (M-2):
            psi = math.atan((-1*t))
            ang.insert(0,psi)
        else:
            psi = ang[0]
            c = math.cos(psi)
            psi = math.atan((-1*t*c))
            ang.insert(0, psi)
    return ang

def FQH(M,t):
    #Stage 0
    q = (3*M)-2
    qc = QuantumCircuit(q)
    for i in range(q):
        if (i % 3) == 0:
            qc.x(i)

    #Stage 1
    ang = psi_angles(M, t)

    for i in range(M-1):
        theta = -2*ang[i]
        target = 3*i + 1
        if i == 0:
            qc.ry(theta, target)
        else:
            cont = 3*i - 1
            cry = RYGate(theta).control(1, ctrl_state='0')
            qc.append(cry, [cont, target])

    #Stage 2
    pi = math.pi
    rz = RZGate(pi)
    for i in range(1, M, 1):    
        n = 1 + ((i-1)*3)
        qc.cx(n, n+1)
        qc.append(rz, [n])
        
    for i in range(1, M, 1):
        n = 2 + ((i-1)*3)
        qc.cx(n, n+1)
        qc.append(rz, [n])
    for i in range(1, M, 1):
        n = 1 + ((i-1)*3)
        qc.cx(n, n-1)

    print(qc)
    return qc

def z_expectations(qc):
    state = Statevector.from_instruction(qc)
    n = qc.num_qubits
    expvals = []

    for j in range(n):
        label = "I" * (n - j - 1) + "Z" + "I" * j
        op = SparsePauliOp.from_list([(label, 1.0)])
        exp = state.expectation_value(op).real
        expvals.append(exp)

    return expvals

M = 5
t = 0.4

qc = FQH(M, t)
print(qc)   


z_vals = z_expectations(qc)

# 1. Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Create the full path for the image
save_path = os.path.join(script_dir, "circuit_diagram.png")

# 3. Draw and Save
fig = qc.draw(output='mpl', style='iqp')
fig.savefig(save_path, dpi=300)
print(f"Circuit diagram saved to: {save_path}")

# Plotting the Expectation Values
plt.figure()
plt.plot(z_vals, 'o-', color='crimson')
plt.title("Z-Pauli Expectation Values")
plt.xlabel("Qubit Index")
plt.ylabel("<Z>")
plt.grid(True)

# Save the graph
graph_path = os.path.join(script_dir, "results_graph.png")
plt.savefig(graph_path, dpi=300)
print(f"Results graph saved to: {graph_path}")
