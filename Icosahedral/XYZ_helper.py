import math
import pandas as pd


def covert_to_xyz(moves_20):
    xyz = pd.DataFrame(0.0, index=range(len(moves_20) + 1), columns=['X', 'Y', 'Z'])
    phi = (1 + math.sqrt(5)) / 2

    movements = {
        1: normalize([0, 1, phi]), 2: normalize([0, -1, phi]),
        3: normalize([0, 1, -phi]), 4: normalize([0, -1, -phi]),
        5: normalize([1, phi, 0]), 6: normalize([-1, phi, 0]),
        7: normalize([1, -phi, 0]), 8: normalize([-1, -phi, 0]),
        9: normalize([phi, 0, 1]), 10: normalize([phi, 0, -1]),
        11: normalize([-phi, 0, 1]), 12: normalize([-phi, 0, -1])
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
