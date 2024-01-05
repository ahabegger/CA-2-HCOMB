import math
import pandas as pd
import numpy as np


def convert_to_xyz(moves_12):
    phi = (1 + math.sqrt(5)) / 2

    # Define movements as a list of normalized vectors
    movements = [
        normalize([0, 1, phi]), normalize([0, -1, phi]),
        normalize([0, 1, -phi]), normalize([0, -1, -phi]),
        normalize([1, phi, 0]), normalize([-1, phi, 0]),
        normalize([1, -phi, 0]), normalize([-1, -phi, 0]),
        normalize([phi, 0, 1]), normalize([phi, 0, -1]),
        normalize([-phi, 0, 1]), normalize([-phi, 0, -1])
    ]

    # Pre-allocate space for xyz coordinates
    xyz = np.zeros((len(moves_12) + 1, 3))

    # Calculate the cumulative sum of movements
    for i, move in enumerate(moves_12):
        xyz[i + 1] = xyz[i] + movements[move - 1]  # -1 because moves are 1-indexed

    return pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])


def is_valid(xyz):
    return xyz.duplicated().sum() == 0


def normalize(vector):
    magnitude = math.sqrt(sum([x ** 2 for x in vector]))
    return [x / magnitude for x in vector]
