import numpy as np
import pandas as pd
import math


def convert_to_xyz(moves_8):
    # Calculate the normalization factor
    norm_factor = 1 / math.sqrt(3)

    # Define movements as a list of vectors
    movements = [
        [norm_factor, norm_factor, norm_factor],
        [-norm_factor, norm_factor, norm_factor],
        [norm_factor, -norm_factor, norm_factor],
        [norm_factor, norm_factor, -norm_factor],
        [-norm_factor, -norm_factor, norm_factor],
        [norm_factor, -norm_factor, -norm_factor],
        [-norm_factor, norm_factor, -norm_factor],
        [-norm_factor, -norm_factor, -norm_factor]
    ]

    # Pre-allocate space for xyz coordinates
    xyz = np.zeros((len(moves_8) + 1, 3))

    # Calculate the cumulative sum of movements
    for i, move in enumerate(moves_8):
        xyz[i + 1] = xyz[i] + movements[move - 1]  # -1 because moves are 1-indexed

    return pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])


def is_valid(xyz):
    return xyz.duplicated().sum() == 0
