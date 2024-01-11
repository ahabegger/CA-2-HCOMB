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

    # Define movements as a list of vectors
    if num_moves == 4:
        return [
            normalize([1, 1, 1]),
            normalize([-1, -1, 1]),
            normalize([-1, 1, -1]),
            normalize([1, -1, -1])
        ]
    elif num_moves == 6:
        return [
            normalize([1, 0, 0]), normalize([-1, 0, 0]),
            normalize([0, 1, 0]), normalize([0, -1, 0]),
            normalize([0, 0, 1]), normalize([0, 0, -1])
        ]
    elif num_moves == 8:
        return [
            normalize([1, 1, 1]),
            normalize([-1, 1, 1]),
            normalize([1, -1, 1]),
            normalize([1, 1, -1]),
            normalize([-1, -1, 1]),
            normalize([1, -1, -1]),
            normalize([-1, 1, -1]),
            normalize([-1, -1, -1])
        ]
    elif num_moves == 12:
        return [
            normalize([0, 1, phi]), normalize([0, -1, phi]),
            normalize([0, 1, -phi]), normalize([0, -1, -phi]),
            normalize([1, phi, 0]), normalize([-1, phi, 0]),
            normalize([1, -phi, 0]), normalize([-1, -phi, 0]),
            normalize([phi, 0, 1]), normalize([phi, 0, -1]),
            normalize([-phi, 0, 1]), normalize([-phi, 0, -1])
        ]
    elif num_moves == 20:
        return [
            normalize([1, 1, 1]), normalize([1, 1, -1]),
            normalize([1, -1, 1]), normalize([1, -1, -1]),
            normalize([-1, 1, 1]), normalize([-1, 1, -1]),
            normalize([-1, -1, 1]), normalize([-1, -1, -1]),
            normalize([0, 1 / phi, phi]), normalize([0, -1 / phi, phi]),
            normalize([0, 1 / phi, -phi]), normalize([0, -1 / phi, -phi]),
            normalize([1 / phi, phi, 0]), normalize([-1 / phi, phi, 0]),
            normalize([1 / phi, -phi, 0]), normalize([-1 / phi, -phi, 0]),
            normalize([phi, 0, 1 / phi]), normalize([-phi, 0, 1 / phi]),
            normalize([phi, 0, -1 / phi]), normalize([-phi, 0, -1 / phi])
        ]


def normalize(vector):
    try:
        magnitude = np.linalg.norm(vector)
        return vector / magnitude
    except:
        magnitude = math.sqrt(sum([x ** 2 for x in vector]))
        return [x / magnitude for x in vector]
