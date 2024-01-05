import math
import pandas as pd
import numpy as np
from Greedy import greedy_lattice
from PDB2Backbone import create_backbone
import Visualization as plot
import XYZHelper as xyz_helper


'''
Tetrahedral.py
This Script is used to create a Tetrahedral (4 Move) Lattice from a PDB file.
'''


def create_tetrahedral(pdb_code):
    backbone_xyz = create_backbone(pdb_code)

    num_rows = backbone_xyz.shape[0]
    cost_df = pd.DataFrame(0.0, index=range(num_rows - 1), columns=range(1, 5))

    # For each row in the backbone_xyz DataFrame
    for i in range(num_rows - 1):
        costs = cost_calculations(backbone_xyz.iloc[i], backbone_xyz.iloc[i + 1])
        cost_df.iloc[i] = costs

    normalize_cost_df = normalize_cost(cost_df)
    initial_moves = [4] * (num_rows - 1)

    norm_factor = 1 / math.sqrt(3)

    # Define movements as a list of vectors
    movements = [
        [norm_factor, norm_factor, norm_factor],
        [-norm_factor, -norm_factor, norm_factor],
        [-norm_factor, norm_factor, -norm_factor],
        [norm_factor, -norm_factor, -norm_factor]
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

    # Distance between unit vector and each of the 4 possible moves
    move_cost = {
        1: np.linalg.norm(unit_vector - np.array([1 / math.sqrt(3), 1 / math.sqrt(3), 1 / math.sqrt(3)])),
        2: np.linalg.norm(unit_vector - np.array([-1 / math.sqrt(3), -1 / math.sqrt(3), 1 / math.sqrt(3)])),
        3: np.linalg.norm(unit_vector - np.array([-1 / math.sqrt(3), 1 / math.sqrt(3), -1 / math.sqrt(3)])),
        4: np.linalg.norm(unit_vector - np.array([1 / math.sqrt(3), -1 / math.sqrt(3), -1 / math.sqrt(3)]))
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
