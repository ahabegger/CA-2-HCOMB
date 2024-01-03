import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def covert_to_xyz(lowest_cost):
    movements = {
        1: [1, 0, 0], 2: [-1, 0, 0], 3: [0, 1, 0],
        4: [0, -1, 0], 5: [0, 0, 1], 6: [0, 0, -1]
    }

    print(lowest_cost)
    return None


def is_valid(xyz):
    copy = xyz
    copy = copy[~(copy == -1000).any(axis=1)]
    rows_are_unique = copy.duplicated().sum() == 0
    return rows_are_unique
