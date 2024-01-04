import math
import numpy as np
import pandas as pd
from PDB2Backbone import create_backbone
import Octahedral.XYZ_helper as xyz_helper
import Visualization as plot
from Octahedral.Greedy import greedy_octahedral

'''
Octahedral.py
This Script is used to create a Octahedral (8 Move) Lattice from a PDB file.
'''


def create_octahedral(pdb_code):
    backbone_xyz = create_backbone(pdb_code)

    num_rows = backbone_xyz.shape[0]
    cost_df = pd.DataFrame(0.0, index=range(num_rows - 1), columns=range(1, 9))

    # For each row in the backbone_xyz DataFrame
    for i in range(num_rows - 1):
        costs = cost_calculations(backbone_xyz.iloc[i], backbone_xyz.iloc[i + 1])
        cost_df.iloc[i] = costs

    normalize_cost_df = normalize_cost(cost_df)
    initial_moves = [1] * (num_rows - 1)

    moves, cost = greedy_octahedral(initial_moves, normalize_cost_df)

    xyz = xyz_helper.convert_to_xyz(moves)
    plot.visualize(xyz, backbone_xyz, title="Octahedral (8 Move) Lattice")

    return xyz


def cost_calculations(input_origin, input_destination):
    origin = np.array([input_origin.X, input_origin.Y, input_origin.Z])
    destination = np.array([input_destination.X, input_destination.Y, input_destination.Z])
    movement_vector = destination - origin
    magnitude = np.linalg.norm(movement_vector)
    unit_vector = movement_vector / magnitude

    # Distance between unit vector and each of the 8 possible moves
    move_cost = {
        1: np.linalg.norm(unit_vector - np.array([1/math.sqrt(3), 1/math.sqrt(3), 1/math.sqrt(3)])),
        2: np.linalg.norm(unit_vector - np.array([-1/math.sqrt(3), 1/math.sqrt(3), 1/math.sqrt(3)])),
        3: np.linalg.norm(unit_vector - np.array([1/math.sqrt(3), -1/math.sqrt(3), 1/math.sqrt(3)])),
        4: np.linalg.norm(unit_vector - np.array([1/math.sqrt(3), 1/math.sqrt(3), -1/math.sqrt(3)])),
        5: np.linalg.norm(unit_vector - np.array([-1/math.sqrt(3), -1/math.sqrt(3), 1/math.sqrt(3)])),
        6: np.linalg.norm(unit_vector - np.array([1/math.sqrt(3), -1/math.sqrt(3), -1/math.sqrt(3)])),
        7: np.linalg.norm(unit_vector - np.array([-1/math.sqrt(3), 1/math.sqrt(3), -1/math.sqrt(3)])),
        8: np.linalg.norm(unit_vector - np.array([-1/math.sqrt(3), -1/math.sqrt(3), -1/math.sqrt(3)]))
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
