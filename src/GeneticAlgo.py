import numpy as np


def mutateCoefs(coefs):
    newCoefs = []
    for array in coefs:
        newCoefs.append(np.copy(array))
    for i in range(len(newCoefs)):
        for row in range(len(newCoefs[i])):
            for col in range(len(newCoefs[i][row])):
                newCoefs[i][row][col] = np.random.normal(newCoefs[i][row][col], 1)
    return newCoefs


def mutateIntercepts(intercepts):
    newIntercepts = []
    for array in intercepts:
        newIntercepts.append(np.copy(array))
    for i in range(len(newIntercepts)):
        for row in range(len(newIntercepts[i])):
            newIntercepts[i][row] = np.random.normal(newIntercepts[i][row], 1)
    return newIntercepts
