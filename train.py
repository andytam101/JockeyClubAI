import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim

import numpy as np
from argparse import ArgumentParser

from model import Model

# class Model(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.flatten = nn.Flatten()
#         self.linear_relu_stack = nn.Sequential(
#             nn.Linear(68, 30),
#             nn.ReLU(),
#             nn.Linear(30, 30),
#             nn.ReLU(),
#             nn.Linear(30, 1),
#             nn.ReLU()
#         )

#     def forward(self, x):
#         x = self.flatten(x)
#         logits = self.linear_relu_stack(x)
#         return logits


# def train(x, y, epochs=100, lr=0.001):
#     dataset = TensorDataset(x, y)
#     dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
#     loss_fn = nn.MSELoss()

#     model = Model()
#     optimizer = optim.SGD(model.parameters(), lr=lr)

#     for epoch in range(epochs):
#         for batch_X, batch_y in dataloader:
#             pred_y = model(batch_X)
#             loss = loss_fn(pred_y, batch_y)
#             optimizer.zero_grad()
#             loss.backward()

#             optimizer.step()
        
#         if (epoch + 1) % 10 == 0:
#             print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")    


def get_data(input_file, output_file):
    x = np.load(input_file)[:1]
    y = np.load(output_file)[:1,]
    return torch.tensor(x), torch.tensor(y).unsqueeze(1)


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)

    return parser.parse_args()


def main():
    args = get_args()
    x, y = get_data(args.input, args.output)
    print(x)
    print(y)
    model = Model()
    print("Training...")
    model.train(x, y, lr=0.001)


if __name__ == "__main__":
    main()
