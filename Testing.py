import numpy as np
input = [[5, 2], [2, 5]]
layers = [np.transpose(input)]
print(layers)
previousLayer = np.transpose(input)
print(previousLayer)

print(np.empty([4, 1]))
print(np.zeros([4, 1]))