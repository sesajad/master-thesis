import random

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap
from qiskit.transpiler import PassManagerConfig
from qiskit.transpiler.preset_passmanagers import level_0_pass_manager
from qiskit.providers.fake_provider import ConfigurableFakeBackend

def experiment(n):
    
    target_coupling_map= [[i, i + 1] for i in range(n - 1)] + [[i + 1, i] for i in range(n - 1)]
    
    # swap circuit
    qc = QuantumCircuit(n)
    qc.h(range(0, n))
    
    r = list(range(1, 3))
    random.shuffle(r)
    for i in r:
        if random.choice([True, False]):
            qc.crz(0.5, i, (i+2) % n)
        else:
            qc.cx(i, (i+3) % n)
    qc.toffoli(1, 2, 3)
    

    fig = qc.draw(output='mpl')
    fig.savefig('out/0_original_circuit.png')	

    # transpile circuit
    pm = level_0_pass_manager(PassManagerConfig(basis_gates=['cx', 'u3'], coupling_map=CouplingMap(target_coupling_map)))
    last = qc
    print(len(pm))
    for i, stage in enumerate(pm.stages):
        print(stage)
        stage_pm = pm.__getattribute__(stage)
        if stage_pm:
            last = stage_pm.run(last)
            fig = last.draw(output='mpl', idle_wires=False)
            fig.savefig(f'out/{i+1}_after_{stage}.png')	

if __name__ == '__main__':
    experiment(6)