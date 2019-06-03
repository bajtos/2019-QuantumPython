import numpy as np
import matplotlib.pyplot as plt

from qiskit import IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister, BasicAer, execute
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram

# Define the Quantum and Classical Registers
q = QuantumRegister(3)
# q[0] - the qubit in Alice's lab
# q[1] - the entangled quibit shared by Alice and Bob
# q[2] - the qubit in Bob's lab

# Two classical registers to measure data in Alice's lab
c0 = ClassicalRegister(1, "c0")
c1 = ClassicalRegister(1, "c1")

# plus another classical register to verify teleportation outcome
c2 = ClassicalRegister(1, "c2")

circ = QuantumCircuit(q, c0, c1, c2)

# Initial setup of the teleported qubit
# (Pretty much any U parameters are allowed.)
#circ.u3(0.3,0.2,0.1, q[0])
#circ.x(q[0])

# Entagle Bob's qubit with the shared one
# This creates a Bell state, where the qubits are either 00 or 11
circ.h(q[1])
circ.cx(q[1], q[2])
circ.barrier()

# Alice applies the same operation in reverse on her qubit and the shared one
circ.cx(q[0], q[1]);
circ.h(q[0]);
circ.barrier()

# Alice measures spins
circ.measure(q[0], c0[0])
circ.measure(q[1], c1[0]);

### Alice sends the measured data to Bob ###

# Depending on the data, Bob applies none, X, Y or both transformations
circ.z(q[2]).c_if(c0, 1)
circ.x(q[2]).c_if(c1, 1)

### Voila, qubit was transported. Let's measure it's state
circ.measure(q[2], c2[0]);

# Draw the circuit
circ.draw(output="mpl").savefig("teleportation.png", format="png");

# Execute the circuits
shots = 1024

if True:
    backend = BasicAer.get_backend('qasm_simulator')
else:
    # See https://nbviewer.jupyter.org/github/Qiskit/qiskit-tutorials/blob/master/qiskit/basics/1_getting_started_with_qiskit.ipynb
    IBMQ.load_accounts(hub=None)
    large_enough_devices = IBMQ.backends(filters=lambda x:
            not x.configuration().simulator and
            x.configuration().n_qubits >= 3)
    backend = least_busy(large_enough_devices)

print("Using backend " + backend.name())

job = execute(circ, backend, shots=shots, max_credits=3)
result = job.result()

counts = result.get_counts(circ)
print(counts)
plot_histogram(counts).savefig("teleportation-histogram.png", format="png")
