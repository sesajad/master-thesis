from qiskit.quantum_info.synthesis import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate, SwapGate

decomposer = TwoQubitBasisDecomposer(CXGate())
print(decomposer(CXGate().to_matrix()).draw())

cx_reverse = [[1, 0, 0, 0],
             [0, 0, 0, 1],
             [0, 0, 1, 0],
             [0, 1, 0, 0]]

cx = [[1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 1],
      [0, 0, 1, 0]]


print(decomposer(cx).draw())

print(decomposer(cx_reverse).draw())


print(decomposer(cx @ CXGate().to_matrix()).draw())


print(decomposer(SwapGate().to_matrix()).draw())