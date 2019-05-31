import numpy as np
import matplotlib.pyplot as plt

from qiskit import IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister, BasicAer, execute
from qiskit.providers.ibmq import least_busy

# Define the Quantum and Classical Registers
q = QuantumRegister(1)
c = ClassicalRegister(1)

# Build the circuits
pre = QuantumCircuit(q, c)
# NOT
pre.x(q)
pre.barrier()
meas = QuantumCircuit(q, c)
meas.measure(q, c)
circuits = []
exp_vector = range(1,51)
for exp_index in exp_vector:
    middle = QuantumCircuit(q, c)
    for i in range(45*exp_index):
        # WAIT
        middle.iden(q)
    circuits.append(pre + middle + meas)

circuits[0].draw(output="mpl").savefig("energy-relaxation-circuit.png", format="png");

quit()

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
plt.xlabel('time [45*gate time]')
plt.ylabel('Pr(0)')
plt.grid(True)
plt.show()
