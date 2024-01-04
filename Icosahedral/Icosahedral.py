import numpy as np
import pandas as pd
from PDB2Backbone import create_backbone
import Icosahedral.XYZ_helper as xyz_helper
import Visualization as plot
import math

'''
Icosahedral.py
This Script is used to create a Icosahedral (12 Move) Lattice from a PDB file.
'''


def create_icosahedral(pdb_code):
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

    plot.visualize(lowest_xyz, backbone_xyz, title="Icosahedral (12 Move) Lattice")

    return lowest_xyz


def cost_calculations(input_origin, input_destination):
    origin = np.array([input_origin.X, input_origin.Y, input_origin.Z])
    destination = np.array([input_destination.X, input_destination.Y, input_destination.Z])
    movement_vector = destination - origin
    magnitude = np.linalg.norm(movement_vector)
    unit_vector = movement_vector / magnitude

    phi = (1 + math.sqrt(5)) / 2

    # Distance between unit vector and each of the 12 possible moves
    move_cost = {
        1: np.linalg.norm(unit_vector - normalize(np.array([0, 1, phi]))),
        2: np.linalg.norm(unit_vector - normalize(np.array([0, -1, phi]))),
        3: np.linalg.norm(unit_vector - normalize(np.array([0, 1, -phi]))),
        4: np.linalg.norm(unit_vector - normalize(np.array([0, -1, -phi]))),
        5: np.linalg.norm(unit_vector - normalize(np.array([1, phi, 0]))),
        6: np.linalg.norm(unit_vector - normalize(np.array([-1, phi, 0]))),
        7: np.linalg.norm(unit_vector - normalize(np.array([1, -phi, 0]))),
        8: np.linalg.norm(unit_vector - normalize(np.array([-1, -phi, 0]))),
        9: np.linalg.norm(unit_vector - normalize(np.array([phi, 0, 1]))),
        10: np.linalg.norm(unit_vector - normalize(np.array([phi, 0, -1]))),
        11: np.linalg.norm(unit_vector - normalize(np.array([-phi, 0, 1]))),
        12: np.linalg.norm(unit_vector - normalize(np.array([-phi, 0, -1])))
    }

    return move_cost


def normalize(vector):
    magnitude = np.linalg.norm(vector)
    return vector / magnitude
