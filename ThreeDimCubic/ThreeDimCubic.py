import pandas as pd
import numpy as np
from PDB2Backbone import create_backbone
import ThreeDimCubic.XYZ_helper as xyz_helper
import Visualization as plot


def create_three_dim_cubic(pdb_code):
    backbone_xyz = create_backbone(pdb_code)

    num_rows = backbone_xyz.shape[0]
    cost_df = pd.DataFrame(0.0, index=range(num_rows - 1), columns=range(1, 27))

    # For each row in the backbone_xyz DataFrame
    for i in range(num_rows - 1):
        costs = cost_calculations(backbone_xyz.iloc[i], backbone_xyz.iloc[i + 1])
        cost_df.iloc[i] = costs

    # Find the lowest cost for each row
    lowest_cost = cost_df.idxmin(axis=1)
    lowest_cost = lowest_cost.tolist()

    lowest_xyz = xyz_helper.covert_to_xyz(lowest_cost)

    plot.visualize(lowest_xyz, backbone_xyz)

    return lowest_xyz


def cost_calculations(input_origin, input_destination):
    origin = np.array([input_origin.X, input_origin.Y, input_origin.Z])
    destination = np.array([input_destination.X, input_destination.Y, input_destination.Z])
    movement_vector = destination - origin
    magnitude = np.linalg.norm(movement_vector)
    unit_vector = movement_vector / magnitude

    # Distance between unit vector and each of the 26 possible moves
    move_cost = {
        1: np.linalg.norm(unit_vector - np.array([0, 0, -1])),
        2: np.linalg.norm(unit_vector - np.array([0, 0, 1])),
        3: np.linalg.norm(unit_vector - np.array([0, -1, 0])),
        4: np.linalg.norm(unit_vector - np.array([0, -1, -1])),
        5: np.linalg.norm(unit_vector - np.array([0, -1, 1])),
        6: np.linalg.norm(unit_vector - np.array([0, 1, 0])),
        7: np.linalg.norm(unit_vector - np.array([0, 1, -1])),
        8: np.linalg.norm(unit_vector - np.array([0, 1, 1])),
        9: np.linalg.norm(unit_vector - np.array([-1, 0, 0])),
        10: np.linalg.norm(unit_vector - np.array([-1, 0, -1])),
        11: np.linalg.norm(unit_vector - np.array([-1, 0, 1])),
        12: np.linalg.norm(unit_vector - np.array([-1, -1, 0])),
        13: np.linalg.norm(unit_vector - np.array([-1, -1, -1])),
        14: np.linalg.norm(unit_vector - np.array([-1, -1, 1])),
        15: np.linalg.norm(unit_vector - np.array([-1, 1, 0])),
        16: np.linalg.norm(unit_vector - np.array([-1, 1, -1])),
        17: np.linalg.norm(unit_vector - np.array([-1, 1, 1])),
        18: np.linalg.norm(unit_vector - np.array([1, 0, 0])),
        19: np.linalg.norm(unit_vector - np.array([1, 0, -1])),
        20: np.linalg.norm(unit_vector - np.array([1, 0, 1])),
        21: np.linalg.norm(unit_vector - np.array([1, -1, 0])),
        22: np.linalg.norm(unit_vector - np.array([1, -1, -1])),
        23: np.linalg.norm(unit_vector - np.array([1, -1, 1])),
        24: np.linalg.norm(unit_vector - np.array([1, 1, 0])),
        25: np.linalg.norm(unit_vector - np.array([1, 1, -1])),
        26: np.linalg.norm(unit_vector - np.array([1, 1, 1]))
    }

    # Find the lowest cost for each row
    lowest_cost = min(move_cost.values())
    for key in move_cost.keys():
        move_cost[key] -= abs(lowest_cost)

    return move_cost
