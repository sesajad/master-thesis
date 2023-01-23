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
from qiskit.providers.fake_provider import ConfigurableFakeBackend, FakeBoeblingen

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
    
    # backend
    target_coupling_map= [[i, i + 1] for i in range(n - 1)] + [[i + 1, i] for i in range(n - 1)]
    backend = ConfigurableFakeBackend("linear", version=1, n_qubits=n, coupling_map=target_coupling_map)
    # backend = FakeBoeblingen()
    
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
    logger.critical(f"Transpiled circuit gate count (SWAP): {tqc.count_ops()}")

    # bridge circuit
    qc = QuantumCircuit(n)
    qc.h(range(0, n))
    _linear_chain_gates(qc, n)
    qc.barrier()
    cp = n // 2 - 1
    for i in range(cp):
        qc.cnot(i + 1, i)
        if n - i - 2 >= cp + 1:
            qc.cnot(n - i - 1, n - i - 2)
    for i in range(cp):
        qc.cnot(i, i + 1)
        if n - i - 2 >= cp + 1:
            qc.cnot(n - i - 2, n - i - 1)
    qc.cnot(cp, cp + 1)
    
    for i in range(cp - 1, -1, -1):
        qc.cnot(i, i + 1)
        if n - i - 2 >= cp + 1:
            qc.cnot(n - i - 2, n - i - 1)
    for i in range(cp - 1, -1, -1):
        qc.cnot(i + 1, i)
        if n - i - 2 >= cp + 1:
            qc.cnot(n - i - 1, n - i - 2)
    qc.barrier()
    _linear_chain_gates(qc, n)

    tqc = transpile(qc, backend, initial_layout=range(n))
    fig = tqc.draw(output='mpl', idle_wires=False)
    fig.savefig('out/transpiled_circuit_bridge.png')
    logger.critical(f"Transpiled circuit depth (Bridge): {tqc.depth()}")
    logger.critical(f"Transpiled circuit gate count (Bridge): {tqc.count_ops()}")

if __name__ == '__main__':
    init_log()
    experiment(6)