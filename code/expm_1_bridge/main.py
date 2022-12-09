import logging
import random

def init_log():
    logger = logging.getLogger('results')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('out/results.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeBoeblingen


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
    backend = FakeBoeblingen()
    
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

    # transpiled circuit
    tqc = transpile(qc, backend, initial_layout=range(n))
    fig = tqc.draw(output='mpl', idle_wires=False)
    fig.savefig('out/transpiled_circuit_swap.png')	
    logger.critical(f"Transpiled circuit depth (SWAP): {tqc.depth()}")

    # bridge circuit
    qc = QuantumCircuit(n)
    qc.h(range(0, n))
    _linear_chain_gates(qc, n)
    qc.barrier()
    for i in [*range(n - 2, -1, -1), *range(1, n - 2), *range(n - 2, -1, -1), *range(1, n - 2)]:
        # logger.debug(f"bridging {i}, {i + 1}")
        qc.cnot(i, i + 1)
    qc.barrier()
    _linear_chain_gates(qc, n)

    tqc = transpile(qc, backend, initial_layout=range(n))
    fig = tqc.draw(output='mpl', idle_wires=False)
    fig.savefig('out/transpiled_circuit_bridge.png')
    logger.critical(f"Transpiled circuit depth (Bridge): {tqc.depth()}")

if __name__ == '__main__':
    init_log()
    experiment(4)