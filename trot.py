
from qiskit import QuantumCircuit
import numpy as np

def build_trotter_circuit(B, N, M, t):
    """
    Constructs a Trotterized circuit for the given Hamiltonian dynamics.
    
    Args/parameters:
        B (float): Transverse field parameter.
        N (int): Number of qubits.
        M (int): Number of Trotter steps.
        t (float): Total time for evolution.
    """
    qc = QuantumCircuit(N)
    
    #time calculation
    delta_t = t / M

    angle_x = 2 * B * delta_t
    
    # We need exp(-i * delta_t * Z * Z) -> theta/2 = delta_t -> theta = 2 * delta_t
    angle_zz = 2 * delta_t

    for step in range(M):
        
        # 1. Apply Single-Qubit Terms (Rightmost term in the bracket acts first)
        # Term: product of exp(-i(t/M) * B * X_j)
        for j in range(N):
            qc.rx(angle_x, j)
            
        # 2. Apply Two-Qubit Interaction Terms (Leftmost term in the bracket acts second)
        # Term: product of exp(-i(t/M) * Z_j * Z_{j+1})
        for j in range(N - 1):
            qc.rzz(angle_zz, j, j + 1)
            
        if step < M - 1:
            qc.barrier()

    return qc

#inputs
N_in = 6
M_in = 5
B_in = 0.4
t_in = 2

#circuit construction
circuit = build_trotter_circuit(B_in, N_in, M_in, t_in)

#pringtin
print(circuit)
