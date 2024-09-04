import numpy as np
import csv


def main():
    x = np.load("data.npy")
    y = np.load("times.npy").reshape((x.shape[0], 1))

    table = np.concat((x, y), axis=1)

    f = open("data.csv", "w", newline="")
    writer = csv.writer(f, delimiter=",")
    writer.writerows(table)
    f.close()


if __name__ == "__main__":
    main()