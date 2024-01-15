from Greedy import greedy_lattice
from PDB2Backbone import create_backbone
import Tilt as tilt
import numpy as np

'''
Structures.py
This Script is used to create a Lattice from a PDB file.
'''


def create_lattice(num_moves, pdb_code):
    # Create Backbone
    backbone_xyz = create_backbone(pdb_code)

    # Create Movements
    movements = get_movements(num_moves)

    # Optimize Movements with Tilt.py
    optimized_movements, cost_matrix, structure_cost = tilt.optimize_tilt(backbone_xyz, movements)
    print(f"Optimized Movements: {optimized_movements}")
    print(f"Structure Cost: {structure_cost}")

    xyz, fitted_cost, time = greedy_lattice(cost_matrix, optimized_movements)

    return xyz, structure_cost + fitted_cost, time


def get_movements(num_moves):
    # Define Math Calculations
    sqrt_3_div_2 = np.sqrt(3) / 2
    sqrt_2_div_2 = np.sqrt(2) / 2

    if num_moves == 4:
        # SQUARE TILING (4 MOVES)
        return [
            [1, 0, 0],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0]
        ]
    elif num_moves == 6:
        # CUBIC HONEYCOMB (6 MOVES)
        return [
            [1, 0, 0], [-1, 0, 0],
            [0, 1, 0], [0, -1, 0],
            [0, 0, 1], [0, 0, -1]
        ]
    elif num_moves == 8:
        # TRIANGULAR PRISMATIC HONEYCOMB (8 MOVES)
        return [
            [sqrt_3_div_2, 0.5, 0], [-sqrt_3_div_2, 0.5, 0],
            [0, 1, 0], [sqrt_3_div_2, -0.5, 0],
            [-sqrt_3_div_2, -0.5, 0], [0, -1, 0],
            [0, 0, 1], [0, 0, -1]
        ]
    elif num_moves == 12:
        # TETRAHEDRAL-OCTAHEDRAL HONEYCOMB (12 MOVES)
        return [
            [sqrt_2_div_2, sqrt_2_div_2, 0], [sqrt_2_div_2, 0, sqrt_2_div_2],
            [0, sqrt_2_div_2, sqrt_2_div_2], [-sqrt_2_div_2, -sqrt_2_div_2, 0],
            [-sqrt_2_div_2, 0, -sqrt_2_div_2], [0, -sqrt_2_div_2, -sqrt_2_div_2],
            [sqrt_2_div_2, -sqrt_2_div_2, 0], [sqrt_2_div_2, 0, -sqrt_2_div_2],
            [0, sqrt_2_div_2, -sqrt_2_div_2], [-sqrt_2_div_2, sqrt_2_div_2, 0],
            [-sqrt_2_div_2, 0, sqrt_2_div_2], [0, -sqrt_2_div_2, sqrt_2_div_2]
        ]
