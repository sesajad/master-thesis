import logging
import random

def init_log():
    logger = logging.getLogger('results')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('out/results.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger

from swap_simplifier_pass import SWAPSimplifier

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap
from qiskit.transpiler import PassManagerConfig
from qiskit.transpiler.preset_passmanagers import level_0_pass_manager
from qiskit.providers.fake_provider import ConfigurableFakeBackend

def _linear_chain_gates(qc, n):
    r = list(range(1, n))
    random.shuffle(r)
    for i in r:
        if random.choice([True, False]):
            qc.cx(i-1, i)
        else:
            qc.cx(i, i-1)

def experiment(n):
    logger = logging.getLogger('results')
    
    target_coupling_map= [[i, i + 1] for i in range(n - 1)] + [[i + 1, i] for i in range(n - 1)]
    
    # swap circuit
    qc = QuantumCircuit(n)
    qc.h(range(0, n))
    _linear_chain_gates(qc, n)
    qc.barrier()
    qc.cnot(0, n - 1)
    qc.barrier()
    _linear_chain_gates(qc, n)
    fig = qc.draw(output='mpl')
    fig.savefig('out/original_circuit.png')	
    logger.info(f"Original circuit depth: {qc.depth()}")

    # transpile circuit
    pm = level_0_pass_manager(PassManagerConfig(basis_gates=['cx', 'u3'], coupling_map=CouplingMap(target_coupling_map)))
    pm.routing.append(SWAPSimplifier())
    tqc = pm.run(qc)
    fig = tqc.draw(output='mpl', idle_wires=False)
    fig.savefig('out/transpiled_circuit_swap.png')	
    logger.critical(f"Transpiled circuit depth (SWAP): {tqc.depth()}")
    logger.critical(f"Transpiled circuit gate count (SWAP): {tqc.count_ops()}")

if __name__ == '__main__':
    init_log()
    experiment(6)