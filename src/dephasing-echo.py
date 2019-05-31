import numpy as np
import matplotlib.pyplot as plt

from qiskit import IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister, BasicAer, execute
from qiskit.providers.ibmq import least_busy

# Define the Quantum and Classical Registers
q = QuantumRegister(1)
c = ClassicalRegister(1)

# Build the circuits
pre = QuantumCircuit(q, c)
# HADAMARD
pre.h(q)
pre.barrier()
meas_x = QuantumCircuit(q, c)
meas_x.barrier()
# HADAMARD
meas_x.h(q)
meas_x.measure(q, c)
circuits = []
exp_vector = range(1,51)
for exp_index in exp_vector:
    middle = QuantumCircuit(q, c)
    # wait
    for i in range(15*exp_index):
        middle.iden(q)
    # NOT
    middle.x(q)
    # more wait
    for i in range(15*exp_index):
        middle.iden(q)
    circuits.append(pre + middle + meas_x)

# circuits[0].draw(output="mpl").savefig("dephasing-echo-circuit.png", format="png");

# Execute the circuits
shots = 1024

if False:
    backend = BasicAer.get_backend('statevector_simulator')
elif True:
    backend = BasicAer.get_backend('qasm_simulator')
else:
    # See https://nbviewer.jupyter.org/github/Qiskit/qiskit-tutorials/blob/master/qiskit/basics/1_getting_started_with_qiskit.ipynb
    IBMQ.load_accounts(hub=None)
    large_enough_devices = IBMQ.backends(filters=lambda x: not x.configuration().simulator)
    backend = least_busy(large_enough_devices)

print("Using backend " + backend.name())

job = execute(circuits, backend, shots=shots, max_credits=3)
result = job.result()

# Plot the result
exp_data = []
exp_error = []
for exp_index in exp_vector:
    data = result.get_counts(circuits[exp_index-1])
    try:
        # how often was the qubit measured as |0>
        p0 = data['0']/shots
    except KeyError:
        # data is {'1': 1}, qubit was always in |1>
        p0 = 0
    exp_data.append(p0)
    exp_error.append(np.sqrt(p0*(1-p0)/shots))

plt.errorbar(exp_vector, exp_data, exp_error)
plt.xlabel('time [31*gate time]')
plt.ylabel('Pr(+)')
plt.grid(True)
plt.show()
