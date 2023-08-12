from qiskit.transpiler.basepasses import TransformationPass
from qiskit.dagcircuit import DAGCircuit

class SWAPSimplifier(TransformationPass):
    def __init__(self):
        super().__init__()

    def run(self, dag: DAGCircuit):
        # search for easy (schmidt rank = 2) two-qubit gates
        for node in dag.topological_op_nodes():
            print(node.op)

        return dag  