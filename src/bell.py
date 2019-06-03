from qiskit import IBMQ, QuantumCircuit, QuantumRegister, ClassicalRegister, BasicAer, execute
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram

# Define the Quantum and Classical Registers
q = QuantumRegister(2)
c = ClassicalRegister(2)

# Create a circuit
circ = QuantumCircuit(q, c)

# Create Bell state
circ.h(q[0])
circ.cx(q[0], q[1])

# Measure qubits' values
circ.measure(q, c);

# Draw the circuit
circ.draw(output="mpl").savefig("img/bell-circuit.png", format="png");

# Execute the circuit
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

job = execute(circ, backend, shots=shots, max_credits=3)
result = job.result()

counts = result.get_counts(circ);
print(counts)

diag = plot_histogram(counts)
diag.savefig("img/bell-" + backend.name() + ".png", format="png")
