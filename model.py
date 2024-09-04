import torch
import torch.nn as nn

import numpy as np


class Model:
    def __init__(self):

        self.a0_layer = 68
        self.a1_layer = 30
        self.a2_layer = 30

        self.w0 = torch.rand((self.a0_layer, self.a1_layer))
        # self.w1 = torch.rand((self.a1_layer, self.a2_layer))
        self.w2 = torch.rand((self.a1_layer, 1))

        self.means = None
        self.stds  = None

    def forward_propagation(self, x):
        a0 = x
        z1 = a0 @ self.w0
        a1 = torch.relu(z1)
        print(a1)
        # z2 = a1 @ self.w1
        # a2 = torch.relu(z2)
        z3 = a1 @ self.w2
        a3 = torch.relu(z3)
        return a3
    
    def normalize(self, x):
        if self.means is None:
            self.means = torch.mean(x, dim=0)
            self.stds  = torch.std(x, dim=0)

        return ((x - self.means) / self.stds).nan_to_num(nan=0)

    def cost(self, predict, y):
        return nn.functional.mse_loss(predict, y)

    def relu_derivative(self, x):
        return (x < 0).float()
    
    def sigmoid_derivative(self, x):
        return torch.sigmoid(x) * (1 - torch.sigmoid(x))

    def backpropagation(self, x, y, lr=0.01):
        m = x.shape[0]

        a0 = x
        z1 = a0 @ self.w0
        a1 = torch.relu(z1)
        # z2 = a1 @ self.w1
        # a2 = torch.relu(z2)
        z3 = a1 @ self.w2
        a3 = torch.relu(z3)

        d3 = (a3 - y)       * self.relu_derivative(z3)
        # d2 = d3 @ self.w2.T * self.relu_derivative(z2)
        d1 = d3 @ self.w2.T * self.relu_derivative(z1)

        self.w2 -= lr * a1.T @ d3 / m
        # self.w1 -= lr * a1.T @ d2 / m
        self.w0 -= lr * a0.T @ d1 / m

        return self.cost(a3, y)

    def train(self, x, y, lr=0.01, epochs=10):
        for epoch in range(epochs):
            cost = self.backpropagation(x, y, lr=lr)

            if (epoch+1) % 1 == 0:
                print(f"Epoch {epoch+1}: cost = {cost}")


if __name__ == "__main__":
    model = Model()
    x = torch.tensor(np.load("data.npy")[12345:12348])
    y = torch.tensor(np.load("times.npy")[12345:12348]).unsqueeze(1)

    # print(model.cost(x, y))

    print(model.forward_propagation(x))
    print("=" * 100)
    print(model.backpropagation(x, y, lr=0.1))
    print(model.backpropagation(x, y, lr=0.1))
    print("=" * 100)
    print(model.forward_propagation(x))
