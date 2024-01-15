from Greedy import greedy_lattice
from PDB2Backbone import create_backbone
import Movements
import Tilt as tilt

'''
Structures.py
This Script is used to create a Lattice from a PDB file.
'''


def create_lattice(num_moves, pdb_code):
    # Create Backbone
    backbone_xyz = create_backbone(pdb_code)

    # Create Movements
    movements = Movements.movements(num_moves)

    # Optimize Movements with Tilt.py
    optimized_movements, cost_df = tilt.optimize_tilt(backbone_xyz, movements)
    print(f"Optimized Movements: {optimized_movements}")
    structure_cost = cost_df.min(axis=1).sum()
    print(f"Structure Cost: {structure_cost}")

    # Fit Movements to Lattice
    normalize_cost_df = normalize_cost(cost_df)
    xyz, fitted_cost, time = greedy_lattice(normalize_cost_df, optimized_movements)

    return xyz, structure_cost + fitted_cost, time


def normalize_cost(costs):
    normalize_costs = costs.copy()
    num_rows = costs.shape[0]

    for i in range(num_rows):
        lowest_cost = min(costs.iloc[i])
        for col in costs.columns:
            normalize_costs.at[i, col] -= abs(lowest_cost)

    return normalize_costs
