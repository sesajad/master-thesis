import pennylane as qml
import pennylane.numpy as np

from tqdm import tqdm

dev = qml.device("default.qubit", wires=3)

def initialize(weights):
    qml.Rot(weights[0], weights[1], weights[2], wires=0)
    qml.Rot(weights[3], weights[4], weights[5], wires=1)
    qml.Rot(weights[6], weights[7], weights[8], wires=2)

@qml.qnode(dev)
def variational_instance(initialization, weights):
    initialize(initialization)
    qml.Rot(weights[0], weights[1], weights[2], wires=0)
    qml.Rot(weights[3], weights[4], weights[5], wires=1)
    qml.IsingXX(weights[6], wires=[0, 1])
    qml.Rot(weights[7], weights[8], weights[9], wires=0)
    qml.Rot(weights[10], weights[11], weights[12], wires=1)
    qml.Rot(weights[13], weights[14], weights[15], wires=2)
    qml.IsingXX(weights[16], wires=[1, 2])
    qml.Rot(weights[17], weights[18], weights[19], wires=1)
    qml.Rot(weights[20], weights[21], weights[22], wires=2)
    qml.Rot(weights[23], weights[24], weights[25], wires=0)
    qml.IsingXX(weights[26], wires=[0, 1])
    qml.Rot(weights[27], weights[28], weights[29], wires=0)
    qml.Rot(weights[30], weights[31], weights[32], wires=1)
    qml.Rot(weights[33], weights[34], weights[35], wires=2)
    qml.IsingXX(weights[36], wires=[1, 2])
    qml.Rot(weights[37], weights[38], weights[39], wires=1)
    qml.Rot(weights[40], weights[41], weights[42], wires=2)
    return qml.state()

@qml.qnode(dev)
def target_instance(initialization, alpha):
    initialize(initialization)
    qml.IsingXX(alpha, wires=[0, 2])
    return qml.state()

batch_size = 10

def cost(weights):
    res = []
    for i in range(batch_size):
        init = np.random.uniform(size=(9,), low=-np.pi, high=np.pi)
        alpha = 0.16 * np.pi / 2
        fidelity = qml.qinfo.fidelity(target_instance, variational_instance, [0, 1, 2], [0, 1, 2])((init, alpha), (init, weights))
        res.append(fidelity)
    return - sum(res) / batch_size

window_size = 10

def optimize(init_weights):
    weights = init_weights
    opt = qml.GradientDescentOptimizer()
    fidelities = []
    for i in tqdm(range(1000)):
        weights, fidelity = opt.step_and_cost(cost, weights)
        fidelities.append(fidelity)
        if i % 20 == 0:
            print("Step {}: fidelity = {}".format(i, np.mean(fidelities[-window_size:])))
            print("Weights: {}".format(weights[[6,16,26,36]] / (np.pi / 2)))

        if i % 100 == 0:
            print("All weights: {}".format(weights))

    return weights, fidelities


init_weights = np.random.uniform(size=(43,), low=-np.pi / 4, high=np.pi / 4)
# init_weights[[6,16]] = 0.1 * np.pi / 2 
# init_weights[[26,36]] = -0.1 * np.pi / 2
weights, fidelities = optimize(init_weights)

fidelities = np.convolve(fidelities, np.ones(window_size)/window_size, mode='valid')

