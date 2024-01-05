import numpy as np
import pandas as pd


def convert_to_xyz(moves_6):
    # Define movements as a NumPy array for efficiency
    movements = np.array([
        [0, 0, 0], [1, 0, 0], [-1, 0, 0], [0, 1, 0],
        [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ])

    # Pre-allocate space for xyz coordinates
    xyz = np.zeros((len(moves_6) + 1, 3))

    # Calculate the cumulative sum of movements
    for i, move in enumerate(moves_6):
        xyz[i + 1] = xyz[i] + movements[move]

    return pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])


def is_valid(xyz):
    return xyz.duplicated().sum() == 0
