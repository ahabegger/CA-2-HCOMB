import pandas as pd
import numpy as np


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
    print(convert_xyz([[16.795, 5.303, 9.674], [13.627, 3.183, 9.727], [15.02, 0.524, 7.365], [18.079, 0.067, 9.522],
                       [16.018, -0.068, 12.733], [12.933, -2.098, 11.605], [14.064, -4.074, 8.484],
                       [17.745, -4.827, 9.109],
                       [16.831, -5.403, 12.758], [13.534, -5.884, 14.55], [12.133, -2.832, 16.349],
                       [9.465, -2.07, 18.928],
                       [6.284, -0.393, 17.843], [7.245, 2.792, 19.704], [10.529, 2.849, 17.692], [8.601, 2.542, 14.397],
                       [6.389, 5.4, 15.571], [9.446, 7.567, 16.391], [10.42, 7.402, 12.731], [7.149, 9.149, 11.76],
                       [7.069, 12.816, 10.878], [5.831, 15.204, 13.544], [7.394, -7.701, 21.494],
                       [8.918, -6.884, 18.179],
                       [8.265, -6.161, 14.58], [10.292, -6.606, 11.476], [9.252, -5.359, 8.056], [11.09, -4.713, 4.783],
                       [10.084, -3.274, 1.405], [6.397, -2.394, 0.712], [5.135, -3.901, 4.015], [7.341, -1.52, 5.957],
                       [6.064, 1.417, 3.971], [2.424, 0.208, 4.497], [3.03, -0.068, 8.253], [4.531, 3.441, 8.452],
                       [1.557, 4.706, 6.49], [-0.976, 3.478, 9.087], [1.27, 4.027, 12.181], [2.018, 7.653, 11.246],
                       [-0.756, 10.28, 11.313], [1.302, 13.135, 9.777], [3.307, 10.759, 7.547], [7.02, 10.035, 7.072],
                       [9.707, 11.001, 4.522], [13.164, 9.502, 5.297]]))


def create_one_dim_cubic():
    return None