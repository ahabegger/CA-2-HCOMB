import pandas as pd


def covert_to_xyz(moves_6):
    xyz = pd.DataFrame(0.0, index=range(len(moves_6) + 1), columns=['X', 'Y', 'Z'])
    movements = {
        1: [1, 0, 0], 2: [-1, 0, 0], 3: [0, 1, 0],
        4: [0, -1, 0], 5: [0, 0, 1], 6: [0, 0, -1]
    }

    for i in range(len(moves_6)):
        xyz.iloc[i + 1] = xyz.iloc[i] + movements[moves_6[i]]

    return xyz


def is_valid(xyz):
    copy = xyz
    copy = copy[~(copy == -1000).any(axis=1)]
    rows_are_unique = copy.duplicated().sum() == 0
    return rows_are_unique
