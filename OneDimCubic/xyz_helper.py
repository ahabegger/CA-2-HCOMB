import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def covert_to_xyz(lowest_cost):
    xyz = pd.DataFrame(0.0, index=range(len(lowest_cost) + 1), columns=['X', 'Y', 'Z'])
    movements = {
        1: [1, 0, 0], 2: [-1, 0, 0], 3: [0, 1, 0],
        4: [0, -1, 0], 5: [0, 0, 1], 6: [0, 0, -1]
    }

    for i in range(len(lowest_cost)):
        xyz.iloc[i + 1] = xyz.iloc[i] + movements[lowest_cost[i]]

    return xyz


def is_valid(xyz):
    copy = xyz
    copy = copy[~(copy == -1000).any(axis=1)]
    rows_are_unique = copy.duplicated().sum() == 0
    return rows_are_unique
