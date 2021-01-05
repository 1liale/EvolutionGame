import numpy as np

NN_structure = [3, 6]


def generate_input(player, obstacles, i):
    return np.array([[player.x, obstacles[i].x, obstacles[i].speed]])


def generate_weights_intercepts():
    weights = []
    intercepts = []
    for i in range(len(NN_structure) - 1):
        weights.append(np.random.rand(NN_structure[i], NN_structure[i + 1]) * 2 - 1)
        intercepts.append(np.random.rand(NN_structure[i + 1]) * 2 - 1)
    # print(str(weights) + " " + str(intercepts))
    return weights, intercepts


def produce_output(input, coefs, intercepts):
    # print(str(coefs) + " " + str(intercepts))
    layers = [np.transpose(input)]
    prevLayer = np.transpose(input)
    reduced_layers = NN_structure[1:]
    for i in range(len(reduced_layers)):
        curLayer = np.empty((reduced_layers[i], 1))
        result = np.matmul(np.transpose(coefs[i]), prevLayer) + np.transpose(np.array([intercepts[i]]))
        for j in range(len(curLayer)):
            curLayer[j] = result[j]
        layers.append(curLayer)
        prevLayer = curLayer.copy()

    return layers[-1].tolist().index(max(layers[-1].tolist()))


