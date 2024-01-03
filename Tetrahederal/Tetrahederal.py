import pandas as pd
import numpy as np
from PDB2Backbone import create_backbone
import Visualization as plot
import Tetrahederal.XYZ_helper as xyz_helper


def create_tetrahedral_lattice(pdb_code):
    backbone_xyz = create_backbone(pdb_code)

    num_rows = backbone_xyz.shape[0]
    cost_df = pd.DataFrame(0.0, index=range(num_rows - 1), columns=range(1, 5))

    # For each row in the backbone_xyz DataFrame
    for i in range(num_rows - 1):
        costs = cost_calculations(backbone_xyz.iloc[i], backbone_xyz.iloc[i + 1])
        cost_df.iloc[i] = costs

    print(cost_df)

    # Find the lowest cost for each row
    lowest_cost = cost_df.idxmin(axis=1)
    lowest_cost = lowest_cost.tolist()

    lowest_xyz = xyz_helper.covert_to_xyz(lowest_cost)

    plot.visualize(lowest_xyz, backbone_xyz, title="Tetrahedral Lattice")

    return None


def cost_calculations(input_origin, input_destination):
    return None


if __name__ == "__main__":
    pass
