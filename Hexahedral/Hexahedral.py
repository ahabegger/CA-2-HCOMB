import pandas as pd
from PDB2Backbone import create_backbone
import Hexahedral.XYZ_helper as xyz_helper
import Visualization as plot


def create_one_dim_cubic(pdb_code):
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

    lowest_xyz = xyz_helper.covert_to_xyz(lowest_cost)

    plot.visualize(lowest_xyz, backbone_xyz, title="One Dimensional Cubic Lattice")

    return lowest_xyz


def cost_calculations(input_origin, input_destination):
    moves_dict = {
        1: input_origin.X - input_destination.X,
        2: input_destination.X - input_origin.X,
        3: input_origin.Y - input_destination.Y,
        4: input_destination.Y - input_origin.Y,
        5: input_origin.Z - input_destination.Z,
        6: input_destination.Z - input_origin.Z
    }
    lowest_cost = min(moves_dict.values())
    for key in moves_dict.keys():
        moves_dict[key] += abs(lowest_cost)

    return moves_dict


if __name__ == "__main__":
    pass
