import numpy as np
import pandas as pd


def convert_to_xyz(moves, possible_movements):
    # Pre-allocate space for xyz coordinates
    xyz = np.zeros((len(moves) + 1, 3))

    # Calculate the cumulative sum of movements
    for i, move in enumerate(moves):
        xyz[i + 1] = xyz[i] + possible_movements[move - 1]  # -1 because moves are 1-indexed

    return pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])


def is_valid(xyz):
    return xyz.duplicated().sum() == 0

'''    
# Define movements as a list of vectors
    # Calculate the normalization factor
    norm_factor = 1 / math.sqrt(3)
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
    '''