import numpy as np
import matplotlib.pyplot as plt


def plot(x: np.ndarray, idx, y):
    x_axis = x[:, idx].tolist()
    y_axis = y.tolist()

    plt.scatter(x_axis, y_axis)
    plt.show()


x = np.nan_to_num(np.load("data.npy"), nan=0)
print(x.shape)
y = np.load("times.npy")
plot(x, 27, y)
