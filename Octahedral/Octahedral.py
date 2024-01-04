import math
import numpy as np
import pandas as pd
from PDB2Backbone import create_backbone
import Octahedral.XYZ_helper as xyz_helper
import Visualization as plot

'''
Octahedral.py
This Script is used to create a Octahedral (8 Move) Lattice from a PDB file.
'''


def create_octahedral(pdb_code):
    backbone_xyz = create_backbone(pdb_code)

    num_rows = backbone_xyz.shape[0]
    cost_df = pd.DataFrame(0.0, index=range(num_rows - 1), columns=range(1, 7))

    # For each row in the backbone_xyz DataFrame
    for i in range(num_rows - 1):
        costs = cost_calculations(backbone_xyz.iloc[i], backbone_xyz.iloc[i + 1])
        cost_df.iloc[i] = costs

    print(cost_df)

    # Find the lowest cost for each row
    lowest_cost = cost_df.idxmin(axis=1)
    lowest_cost = lowest_cost.tolist()

    lowest_xyz = xyz_helper.convert_to_xyz(lowest_cost)

    plot.visualize(lowest_xyz, backbone_xyz, title="Octahedral (8 Move) Lattice")

    return lowest_xyz


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
