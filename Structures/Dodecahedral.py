import numpy as np
import pandas as pd
from Greedy import greedy_lattice
from PDB2Backbone import create_backbone
import XYZHelper as xyz_helper
import Visualization as plot
import math

'''
Dodecahedral.py
This Script is used to create a Dodecahedral (20 Move) Lattice from a PDB file.
'''


def create_dodecahedral(pdb_code):
    backbone_xyz = create_backbone(pdb_code)

    num_rows = backbone_xyz.shape[0]
    cost_df = pd.DataFrame(0.0, index=range(num_rows - 1), columns=range(1, 21))

    # For each row in the backbone_xyz DataFrame
    for i in range(num_rows - 1):
        costs = cost_calculations(backbone_xyz.iloc[i], backbone_xyz.iloc[i + 1])
        cost_df.iloc[i] = costs

    print(cost_df)

    normalize_cost_df = normalize_cost(cost_df)
    initial_moves = [1] * (num_rows - 1)

    phi = (1 + math.sqrt(5)) / 2

    # Define movements as a list of normalized vectors
    movements = [
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

    moves, cost = greedy_lattice(initial_moves, normalize_cost_df, movements)
    xyz = xyz_helper.convert_to_xyz(moves, movements)

    return xyz, cost


def cost_calculations(input_origin, input_destination):
    origin = np.array([input_origin.X, input_origin.Y, input_origin.Z])
    destination = np.array([input_destination.X, input_destination.Y, input_destination.Z])
    movement_vector = destination - origin
    magnitude = np.linalg.norm(movement_vector)
    unit_vector = movement_vector / magnitude

    phi = (1 + math.sqrt(5)) / 2

    # Distance between unit vector and each of the 20 possible moves
    move_cost = {
        1: np.linalg.norm(unit_vector - normalize(np.array([1, 1, 1]))),
        2: np.linalg.norm(unit_vector - normalize(np.array([1, 1, -1]))),
        3: np.linalg.norm(unit_vector - normalize(np.array([1, -1, 1]))),
        4: np.linalg.norm(unit_vector - normalize(np.array([1, -1, -1]))),
        5: np.linalg.norm(unit_vector - normalize(np.array([-1, 1, 1]))),
        6: np.linalg.norm(unit_vector - normalize(np.array([-1, 1, -1]))),
        7: np.linalg.norm(unit_vector - normalize(np.array([-1, -1, 1]))),
        8: np.linalg.norm(unit_vector - normalize(np.array([-1, -1, -1]))),
        9: np.linalg.norm(unit_vector - normalize(np.array([0, 1 / phi, phi]))),
        10: np.linalg.norm(unit_vector - normalize(np.array([0, -1 / phi, phi]))),
        11: np.linalg.norm(unit_vector - normalize(np.array([0, 1 / phi, -phi]))),
        12: np.linalg.norm(unit_vector - normalize(np.array([0, -1 / phi, -phi]))),
        13: np.linalg.norm(unit_vector - normalize(np.array([1 / phi, phi, 0]))),
        14: np.linalg.norm(unit_vector - normalize(np.array([-1 / phi, phi, 0]))),
        15: np.linalg.norm(unit_vector - normalize(np.array([1 / phi, -phi, 0]))),
        16: np.linalg.norm(unit_vector - normalize(np.array([-1 / phi, -phi, 0]))),
        17: np.linalg.norm(unit_vector - normalize(np.array([phi, 0, 1 / phi]))),
        18: np.linalg.norm(unit_vector - normalize(np.array([-phi, 0, 1 / phi]))),
        19: np.linalg.norm(unit_vector - normalize(np.array([phi, 0, -1 / phi]))),
        20: np.linalg.norm(unit_vector - normalize(np.array([-phi, 0, -1 / phi])))
    }

    return move_cost


def normalize(vector):
    try:
        magnitude = np.linalg.norm(vector)
        return vector / magnitude
    except:
        magnitude = math.sqrt(sum([x ** 2 for x in vector]))
        return [x / magnitude for x in vector]


def normalize_cost(costs):
    normalize_costs = costs.copy()
    num_rows = costs.shape[0]

    for i in range(num_rows):
        lowest_cost = min(costs.iloc[i])
        for col in costs.columns:
            normalize_costs.at[i, col] -= abs(lowest_cost)

    return normalize_costs
