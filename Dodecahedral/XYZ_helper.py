import math
import pandas as pd


def convert_to_xyz(moves_20):
    xyz = pd.DataFrame(0.0, index=range(len(moves_20) + 1), columns=['X', 'Y', 'Z'])
    phi = (1 + math.sqrt(5)) / 2

    movements = {
        1: normalize([1, 1, 1]), 2: normalize([1, 1, -1]),
        3: normalize([1, -1, 1]), 4: normalize([1, -1, -1]),
        5: normalize([-1, 1, 1]), 6: normalize([-1, 1, -1]),
        7: normalize([-1, -1, 1]), 8: normalize([-1, -1, -1]),
        9: normalize([0, 1 / phi, phi]), 10: normalize([0, -1 / phi, phi]),
        11: normalize([0, 1 / phi, -phi]), 12: normalize([0, -1 / phi, -phi]),
        13: normalize([1 / phi, phi, 0]), 14: normalize([-1 / phi, phi, 0]),
        15: normalize([1 / phi, -phi, 0]), 16: normalize([-1 / phi, -phi, 0]),
        17: normalize([phi, 0, 1 / phi]), 18: normalize([-phi, 0, 1 / phi]),
        19: normalize([phi, 0, -1 / phi]), 20: normalize([-phi, 0, -1 / phi])
    }

    for i in range(len(moves_20)):
        xyz.iloc[i + 1] = xyz.iloc[i] + movements[moves_20[i]]

    return xyz


def is_valid(xyz):
    copy = xyz
    copy = copy[~(copy == -1000).any(axis=1)]
    rows_are_unique = copy.duplicated().sum() == 0
    return rows_are_unique


def normalize(vector):
    magnitude = math.sqrt(sum([x ** 2 for x in vector]))
    return [x / magnitude for x in vector]
