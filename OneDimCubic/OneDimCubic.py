import pandas as pd
import numpy as np
from PDB2Backbone import create_backbone


def create_one_dim_cubic(pdb_code):
    backbone_xyz = create_backbone(pdb_code)

    return backbone_xyz


def convert_xyz(input_xyz):
    # Preparing Input
    input_df = pd.DataFrame(input_xyz)
    input_df.columns = ['x', 'y', 'z']
    num_rows, num_columns = input_df.shape

    output_df = pd.DataFrame(-1000, index=range(num_rows), columns=input_df.columns)
    priority_df = pd.DataFrame(0, index=range(num_rows - 1), columns=range(6))

    for origin in range(num_rows - 1):
        destination = origin + 1
        priority = move_priority(input_df.iloc[origin], input_df.iloc[destination])
        priority_df.iloc[origin] = priority

    # Determine the First Point
    output_df.iloc[0] = np.floor(input_df.iloc[0] - (input_df.iloc[0] % 3)).astype(int)

    movements = {
        1: [1, 0, 0], 2: [-1, 0, 0], 3: [0, 1, 0],
        4: [0, -1, 0], 5: [0, 0, 1], 6: [0, 0, -1]
    }

    print(priority_df)

    print(is_valid(output_df))

    # Determine Next Point
    for index, row in input_df.iterrows():

        if not is_valid(output_df):
            break

    print("Correction needed")

    return output_df


def is_valid(xyz):
    copy = xyz
    copy = copy[~(copy == -1000).any(axis=1)]
    rows_are_unique = copy.duplicated().sum() == 0
    return rows_are_unique


def move_priority(input_origin, input_destination):
    moves_dict = {
        1: input_origin.x - input_destination.x,
        2: input_destination.x - input_origin.x,
        3: input_origin.y - input_destination.y,
        4: input_destination.y - input_origin.y,
        5: input_origin.z - input_destination.z,
        6: input_destination.z - input_origin.z
    }
    return sorted(moves_dict, key=moves_dict.get)


if __name__ == "__main__":
    pass
