import numpy as np
import torch
from tqdm import tqdm
from loader import DataLoader

import csv

from db import DataBase


# weights = torch.rand((54, 1), dtype=torch.float32)
weights = torch.load("linear_reg_300000.pt")


def cost(x, y):
    return torch.nn.functional.mse_loss(predict(x), y)


def predict(x):
    return x @ weights


def gradient_descent(x, y, iterations, lr=0.1):
    global weights
    m = x.size()[0]
    for i in tqdm(range(iterations), desc="Training"):
        p = predict(x)
        diff = p - y
        weights -= lr * (2 * (x.T @ diff) / m)


def train(iterations=300000):
    x = torch.tensor(np.nan_to_num(np.load("data.npy"), nan=0))
    y = torch.tensor(np.load("times.npy")).unsqueeze(1)

    sample_x = x[:, :]
    sample_y = y[:]   

    gradient_descent(sample_x, sample_y, iterations, lr=0.00007)
    print(f"Final cost: {(cost(sample_x, sample_y))}")

    torch.save(weights, f"linear_reg_{iterations}.pt")


def main():
    f = open("test.csv", "w", newline="")
    writer = csv.writer(f, delimiter=",")

    db = DataBase("sqlite:///data.db")
    print("preparing data loader...")
    loader = DataLoader(db)
    
    ps = db.get_all_participations_for_race(2024, 821)

    writer.writerow(map(lambda x: x.horseId, ps))
    writer.writerow(map(lambda x: x.finalTime, ps))

    x = np.zeros((len(ps), 54), dtype=np.float32)
    for idx, p in enumerate(ps):
        x[idx] = loader.load_participation(p)
    
    x = torch.tensor(x)

    y = predict(x)
    # print(torch.squeeze(y, 1))
    writer.writerow(torch.squeeze(y, 1).tolist())
    f.close()

if __name__ == "__main__":
    main()