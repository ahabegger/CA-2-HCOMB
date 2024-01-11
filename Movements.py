# Import Outside Libraries
import math
import numpy as np


'''
Movements.py
This Script is as a library of movements for the Structures.py script.
'''


def movements(num_moves):
    # Define Math Constants
    phi = (1 + math.sqrt(5)) / 2
    norm_factor = 1 / math.sqrt(3)

    # Define movements as a list of vectors
    if num_moves == 4:
        return [
            [norm_factor, norm_factor, norm_factor],
            [-norm_factor, -norm_factor, norm_factor],
            [-norm_factor, norm_factor, -norm_factor],
            [norm_factor, -norm_factor, -norm_factor]
        ]
    elif num_moves == 6:
        return [
            [1, 0, 0], [-1, 0, 0],
            [0, 1, 0], [0, -1, 0],
            [0, 0, 1], [0, 0, -1]
        ]
    elif num_moves == 8:
        return [
            [norm_factor, norm_factor, norm_factor],
            [-norm_factor, norm_factor, norm_factor],
            [norm_factor, -norm_factor, norm_factor],
            [norm_factor, norm_factor, -norm_factor],
            [-norm_factor, -norm_factor, norm_factor],
            [norm_factor, -norm_factor, -norm_factor],
            [-norm_factor, norm_factor, -norm_factor],
            [-norm_factor, -norm_factor, -norm_factor]
        ]
    elif num_moves == 12:
        return [
            [0, 1, phi], [0, -1, phi],
            [0, 1, -phi], [0, -1, -phi],
            [1, phi, 0], [-1, phi, 0],
            [1, -phi, 0], [-1, -phi, 0],
            [phi, 0, 1], [phi, 0, -1],
            [-phi, 0, 1], [-phi, 0, -1]
        ]
    elif num_moves == 20:
        return [
            [1, 1, 1], [1, 1, -1],
            [1, -1, 1], [1, -1, -1],
            [-1, 1, 1], [-1, 1, -1],
            [-1, -1, 1], [-1, -1, -1],
            [0, 1 / phi, phi], [0, -1 / phi, phi],
            [0, 1 / phi, -phi], [0, -1 / phi, -phi],
            [1 / phi, phi, 0], [-1 / phi, phi, 0],
            [1 / phi, -phi, 0], [-1 / phi, -phi, 0],
            [phi, 0, 1 / phi], [-phi, 0, 1 / phi],
            [phi, 0, -1 / phi], [-phi, 0, -1 / phi]
        ]


def normalize(vector):
    try:
        magnitude = np.linalg.norm(vector)
        return vector / magnitude
    except:
        magnitude = math.sqrt(sum([x ** 2 for x in vector]))
        return [x / magnitude for x in vector]
