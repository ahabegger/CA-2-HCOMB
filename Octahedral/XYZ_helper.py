import pandas as pd
import math


def convert_to_xyz(moves_8):
    xyz = pd.DataFrame(0.0, index=range(len(moves_8) + 1), columns=['X', 'Y', 'Z'])

    movements = {
        1: [1 / math.sqrt(3), 1 / math.sqrt(3), 1 / math.sqrt(3)],
        2: [-1 / math.sqrt(3), 1 / math.sqrt(3), 1 / math.sqrt(3)],
        3: [1 / math.sqrt(3), -1 / math.sqrt(3), 1 / math.sqrt(3)],
        4: [1 / math.sqrt(3), 1 / math.sqrt(3), -1 / math.sqrt(3)],
        5: [-1 / math.sqrt(3), -1 / math.sqrt(3), 1 / math.sqrt(3)],
        6: [1 / math.sqrt(3), -1 / math.sqrt(3), -1 / math.sqrt(3)],
        7: [-1 / math.sqrt(3), 1 / math.sqrt(3), -1 / math.sqrt(3)],
        8: [-1 / math.sqrt(3), -1 / math.sqrt(3), -1 / math.sqrt(3)]
    }

    for i in range(len(moves_8)):
        xyz.iloc[i + 1] = xyz.iloc[i] + movements[moves_8[i]]

    return xyz


def is_valid(xyz):
    copy = xyz
    copy = copy[~(copy == -1000).any(axis=1)]
    rows_are_unique = copy.duplicated().sum() == 0
    return rows_are_unique
