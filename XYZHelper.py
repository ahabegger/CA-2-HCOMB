# Import Outside Libraries
import numpy as np
import pandas as pd
import math

'''
XYZHelper.py
This Script is used to convert a list of moves into a DataFrame of xyz coordinates 
and to check if the xyz coordinates are valid.
'''


def convert_to_xyz(moves, possible_movements):
    # Ensure moves is a NumPy array
    moves = np.array(moves, dtype=int) - 1  # Adjust for 1-indexing

    # Check if possible_movements is a list of lists or a 2D NumPy array
    if isinstance(possible_movements, list):
        possible_movements = np.array(possible_movements)

    # Initialize the xyz array with the origin and correct size
    xyz = np.zeros((len(moves) + 1, 3))

    # Efficiently compute the cumulative sum of movements
    xyz[1:] = np.cumsum(possible_movements[moves], axis=0)

    return pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])


def is_valid(xyz):
    return not xyz.duplicated().any()


def normalize(vector):
    magnitude = np.linalg.norm(vector)
    return vector / magnitude
