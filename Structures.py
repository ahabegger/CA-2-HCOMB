from Greedy import greedy_lattice
from PDB2Backbone import create_backbone
import Tilt as tilt
import numpy as np
import time

'''
Structures.py
This Script is used to create a Lattice from a PDB file.
'''


def create_lattice(num_moves, pdb_code):
    # Create Backbone
    backbone_xyz = create_backbone(pdb_code)

    # Get Structure Name and Movements
    structure_name, movements = get_movements(num_moves)

    print('-' * 50)
    print(f"{structure_name} ({num_moves} Moves) for {pdb_code}")

    # Optimize Movements with Tilt.py
    print('-' * 50)
    print("TILT OPTIMIZATION")
    start_time = time.time()
    optimized_movements, cost_matrix, structure_cost, rotations = tilt.optimize_tilt(backbone_xyz, movements)
    tilt_time = time.time() - start_time
    print(f"Rotations: {rotations[0]} around X-Axis, {rotations[1]} around Y-Axis, {rotations[2]} around Z-Axis")
    print(f"Structure Cost: {structure_cost}")
    print(f"Tilt Time: {tilt_time}")

    # Fit Points with Greedy.py
    print('-' * 50)
    print("GREEDY FITTING OPTIMIZATION")
    start_time = time.time()
    xyz, fitted_cost = greedy_lattice(cost_matrix, optimized_movements)
    fitted_time = time.time() - start_time
    print(f"Fitting Cost: {fitted_cost}")
    print(f"Fitting Time: {fitted_time}")

    # Summarize Results
    print('-' * 50)
    print(f"Total Cost: {structure_cost + fitted_cost}")
    print(f"Total Time: {tilt_time + fitted_time}")
    print('-' * 50)

    return xyz, structure_cost + fitted_cost, time


def get_movements(num_moves):
    # Define Math Calculations
    sqrt_3_div_2 = np.sqrt(3) / 2
    sqrt_2_div_2 = np.sqrt(2) / 2

    if num_moves == 4:
        return ("SQUARE TILING",
                [
                    [1, 0, 0],
                    [-1, 0, 0],
                    [0, 1, 0],
                    [0, -1, 0]
                ])
    elif num_moves == 6:
        return ("CUBIC HONEYCOMB",
                [
                    [1, 0, 0], [-1, 0, 0],
                    [0, 1, 0], [0, -1, 0],
                    [0, 0, 1], [0, 0, -1]
                ])
    elif num_moves == 8:
        # TRIANGULAR PRISMATIC HONEYCOMB (8 MOVES)
        return ("TRIANGULAR PRISMATIC HONEYCOMB",
                [
                    [sqrt_3_div_2, 0.5, 0], [-sqrt_3_div_2, 0.5, 0],
                    [0, 1, 0], [sqrt_3_div_2, -0.5, 0],
                    [-sqrt_3_div_2, -0.5, 0], [0, -1, 0],
                    [0, 0, 1], [0, 0, -1]
                ])
    elif num_moves == 12:
        # TETRAHEDRAL-OCTAHEDRAL HONEYCOMB (12 MOVES)
        return ("TETRAHEDRAL-OCTAHEDRAL HONEYCOMB",
                [
                    [sqrt_2_div_2, sqrt_2_div_2, 0], [sqrt_2_div_2, 0, sqrt_2_div_2],
                    [0, sqrt_2_div_2, sqrt_2_div_2], [-sqrt_2_div_2, -sqrt_2_div_2, 0],
                    [-sqrt_2_div_2, 0, -sqrt_2_div_2], [0, -sqrt_2_div_2, -sqrt_2_div_2],
                    [sqrt_2_div_2, -sqrt_2_div_2, 0], [sqrt_2_div_2, 0, -sqrt_2_div_2],
                    [0, sqrt_2_div_2, -sqrt_2_div_2], [-sqrt_2_div_2, sqrt_2_div_2, 0],
                    [-sqrt_2_div_2, 0, sqrt_2_div_2], [0, -sqrt_2_div_2, sqrt_2_div_2]
                ])
