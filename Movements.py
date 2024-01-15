import numpy as np

'''
Movements.py
This Script is as a library of movements for the Structures.py script.
'''


def movements(num_moves):
    # Define Math Calculations
    sqrt_3_div_2 = np.sqrt(3) / 2
    sqrt_2_div_2 = np.sqrt(2) / 2

    if num_moves == 4:
        # SQUARE TILING (4 MOVES)
        return [
            [1, 0, 0],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0]
        ]
    elif num_moves == 6:
        # CUBIC HONEYCOMB (6 MOVES)
        return [
            [1, 0, 0], [-1, 0, 0],
            [0, 1, 0], [0, -1, 0],
            [0, 0, 1], [0, 0, -1]
        ]
    elif num_moves == 8:
        # TRIANGULAR PRISMATIC HONEYCOMB (8 MOVES)
        return [
            [sqrt_3_div_2, 0.5, 0], [-sqrt_3_div_2, 0.5, 0],
            [0, 1, 0], [sqrt_3_div_2, -0.5, 0],
            [-sqrt_3_div_2, -0.5, 0], [0, -1, 0],
            [0, 0, 1], [0, 0, -1]
        ]
    elif num_moves == 12:
        # TETRAHEDRAL-OCTAHEDRAL HONEYCOMB (12 MOVES)
        return [
            [sqrt_2_div_2, sqrt_2_div_2, 0], [sqrt_2_div_2, 0, sqrt_2_div_2],
            [0, sqrt_2_div_2, sqrt_2_div_2], [-sqrt_2_div_2, -sqrt_2_div_2, 0],
            [-sqrt_2_div_2, 0, -sqrt_2_div_2], [0, -sqrt_2_div_2, -sqrt_2_div_2],
            [sqrt_2_div_2, -sqrt_2_div_2, 0], [sqrt_2_div_2, 0, -sqrt_2_div_2],
            [0, sqrt_2_div_2, -sqrt_2_div_2], [-sqrt_2_div_2, sqrt_2_div_2, 0],
            [-sqrt_2_div_2, 0, sqrt_2_div_2], [0, -sqrt_2_div_2, sqrt_2_div_2]
        ]
