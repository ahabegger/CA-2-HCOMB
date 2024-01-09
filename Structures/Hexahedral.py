# Import Outside Libraries
import numpy as np
import pandas as pd

# Import Local Libraries
from PDB2Backbone import create_backbone
import XYZHelper as xyz_helper
from Greedy import greedy_lattice

'''
Hexahedral.py
This Script is used to create a Hexahedral (6 Move) Lattice from a PDB file.
'''


def create_hexahedral(pdb_code):
    backbone_xyz = create_backbone(pdb_code)

    num_rows = backbone_xyz.shape[0]
    cost_df = pd.DataFrame(0.0, index=range(num_rows - 1), columns=range(1, 7))

    # For each row in the backbone_xyz DataFrame
    for i in range(num_rows - 1):
        costs = cost_calculations(backbone_xyz.iloc[i], backbone_xyz.iloc[i + 1])
        cost_df.iloc[i] = costs

    normalize_cost_df = normalize_cost(cost_df)

    movements = np.array([
        [1, 0, 0], [-1, 0, 0], [0, 1, 0],
        [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ])

    moves, cost, time = greedy_lattice(normalize_cost_df, movements)
    xyz = xyz_helper.convert_to_xyz(moves, movements)

    return xyz, cost, time


def cost_calculations(input_origin, input_destination):
    origin = np.array([input_origin.X, input_origin.Y, input_origin.Z])
    destination = np.array([input_destination.X, input_destination.Y, input_destination.Z])
    movement_vector = destination - origin
    magnitude = np.linalg.norm(movement_vector)
    unit_vector = movement_vector / magnitude

    # Distance between unit vector and each of the 6 possible moves
    move_cost = {
        1: np.linalg.norm(unit_vector - np.array([1, 0, 0])),
        2: np.linalg.norm(unit_vector - np.array([-1, 0, 0])),
        3: np.linalg.norm(unit_vector - np.array([0, 1, 0])),
        4: np.linalg.norm(unit_vector - np.array([0, -1, 0])),
        5: np.linalg.norm(unit_vector - np.array([0, 0, 1])),
        6: np.linalg.norm(unit_vector - np.array([0, 0, -1]))
    }

    return move_cost


def normalize_cost(costs):
    normalize_costs = costs.copy()
    num_rows = costs.shape[0]

    for i in range(num_rows):
        lowest_cost = min(costs.iloc[i])
        for col in costs.columns:
            normalize_costs.at[i, col] -= abs(lowest_cost)

    return normalize_costs
