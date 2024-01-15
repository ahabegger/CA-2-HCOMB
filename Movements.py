# Import Outside Libraries
import math
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
            normalize([1, 0, 0]),
            normalize([-1, 0, 0]),
            normalize([0, 1, 0]),
            normalize([0, -1, 0])
        ]
    elif num_moves == 6:
        # CUBIC HONEYCOMB (6 MOVES)
        return [
            normalize([1, 0, 0]), normalize([-1, 0, 0]),
            normalize([0, 1, 0]), normalize([0, -1, 0]),
            normalize([0, 0, 1]), normalize([0, 0, -1])
        ]
    elif num_moves == 8:
        # TRIANGULAR PRISMATIC HONEYCOMB (8 MOVES)
        return [
            normalize([sqrt_3_div_2, 0.5, 0]), normalize([-sqrt_3_div_2, 0.5, 0]),
            normalize([0, 1, 0]), normalize([sqrt_3_div_2, -0.5, 0]),
            normalize([-sqrt_3_div_2, -0.5, 0]), normalize([0, -1, 0]),
            normalize([0, 0, 1]), normalize([0, 0, -1])
        ]
    elif num_moves == 12:
        # TETRAHEDRAL-OCTAHEDRAL HONEYCOMB (12 MOVES)
        return [
            normalize([sqrt_2_div_2, sqrt_2_div_2, 0]), normalize([sqrt_2_div_2, 0, sqrt_2_div_2]),
            normalize([0, sqrt_2_div_2, sqrt_2_div_2]), normalize([-sqrt_2_div_2, -sqrt_2_div_2, 0]),
            normalize([-sqrt_2_div_2, 0, -sqrt_2_div_2]), normalize([0, -sqrt_2_div_2, -sqrt_2_div_2]),
            normalize([sqrt_2_div_2, -sqrt_2_div_2, 0]), normalize([sqrt_2_div_2, 0, -sqrt_2_div_2]),
            normalize([0, sqrt_2_div_2, -sqrt_2_div_2]), normalize([-sqrt_2_div_2, sqrt_2_div_2, 0]),
            normalize([-sqrt_2_div_2, 0, sqrt_2_div_2]), normalize([0, -sqrt_2_div_2, sqrt_2_div_2])
        ]


def normalize(vector):
    try:
        magnitude = np.linalg.norm(vector)
        return vector / magnitude
    except:
        magnitude = math.sqrt(sum([x ** 2 for x in vector]))
        return [x / magnitude for x in vector]
