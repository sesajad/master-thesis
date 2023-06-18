from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter, SuzukiTrotter

n = 5
e = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 2), (1, 3), (0, 4)]

labels = []
for i, j in e:
    label = ['I'] * n
    label[i] = 'Z'
    label[j] = 'Z'
    labels.append(''.join(label))

hamiltonian = SparsePauliOp(labels)

time = 1.0
evo = PauliEvolutionGate(hamiltonian, time=0.2)

circuit = QuantumCircuit(n)
circuit.append(evo, range(n))
print(circuit.draw())

print(LieTrotter(2).synthesize(evo).decompose().draw())

print(SuzukiTrotter().synthesize(evo).decompose().draw())