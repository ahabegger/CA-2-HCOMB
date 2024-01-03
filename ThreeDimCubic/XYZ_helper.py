import pandas as pd


def covert_to_xyz(moves_26):
    xyz = pd.DataFrame(0.0, index=range(len(moves_26) + 1), columns=['X', 'Y', 'Z'])
    movements = {
        1: [0, 0, -1], 2: [0, 0, 1],
        3: [0, -1, 0], 4: [0, -1, -1], 5: [0, -1, 1],
        6: [0, 1, 0], 7: [0, 1, -1], 8: [0, 1, 1],
        9: [-1, 0, 0], 10: [-1, 0, -1], 11: [-1, 0, 1],
        12: [-1, -1, 0], 13: [-1, -1, -1], 14: [-1, -1, 1],
        15: [-1, 1, 0], 16: [-1, 1, -1], 17: [-1, 1, 1],
        18: [1, 0, 0], 19: [1, 0, -1], 20: [1, 0, 1],
        21: [1, -1, 0], 22: [1, -1, -1], 23: [1, -1, 1],
        24: [1, 1, 0], 25: [1, 1, -1], 26: [1, 1, 1]
    }

    for i in range(len(moves_26)):
        xyz.iloc[i + 1] = xyz.iloc[i] + movements[moves_26[i]]

    return xyz


def is_valid(xyz):
    copy = xyz
    copy = copy[~(copy == -1000).any(axis=1)]
    rows_are_unique = copy.duplicated().sum() == 0
    return rows_are_unique
