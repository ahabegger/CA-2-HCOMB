"""
Structures.py
Generate a structure based on the input parameters like the number of moves and a PDB file,
then optimize the structure using tilt and fitting algorithms. The code begins by
constructing a CA trace structure from a PDB file, defines movements based on the number
of moves, and then applies optimization techniques to refine the structure, finally
returning the optimized XYZ coordinates.
"""

import time
import numpy as np
import pandas as pd
import Tilting as tilt
from Fitting import fitting_algorithm
from PDB2CA import create_trace


def create_structure(num_moves, pdb_filepath, pdb_code, multiprocess_toggle):
    """
    Create a structure based on the input parameters like the number of moves and a PDB file,
    then optimize the structure using tilt and fitting algorithms.
    :param num_moves:
    :param pdb_filepath:
    :param pdb_code:
    :param multiprocess_toggle:
    :return: xyz
    """

    # Create CA Trace and Get Amino Acid Distance
    ca_trace = create_trace(pdb_filepath)
    amino_acid_distance = get_amino_acid_distance(ca_trace[['X', 'Y', 'Z']])

    # Get Structure Name and Movements
    structure_name, movements = get_movements(num_moves)
    movements = np.array(movements, dtype=np.float16)

    print('-' * 50)
    print(f"{structure_name} ({num_moves} Moves) for {pdb_code}")

    # Optimize Movements with Tilting.py
    print('-' * 50)
    print("TILT OPTIMIZATION")
    start_time = time.time()
    optimized_movements, cost_matrix, structure_cost, rotations = tilt.optimize_tilt(ca_trace, movements)
    tilt_time = time.time() - start_time
    print(f"Rotations: {rotations[0]} around X-Axis, {rotations[1]} around Y-Axis, {rotations[2]} around Z-Axis")
    print(f"Structure Cost: {structure_cost}")
    print(f"Tilt Time: {tilt_time}")

    # Fit Points with Fitting.py
    print('-' * 50)
    print("FITTING OPTIMIZATION")
    start_time = time.time()
    fitted_moves, fitted_cost = fitting_algorithm(cost_matrix, optimized_movements, multiprocess_toggle)
    fitted_time = time.time() - start_time
    print(f"Fitting Cost: {fitted_cost}")
    print(f"Fitting Time: {fitted_time}")

    # Determine XYZ Coordinates
    xyz = convert_to_xyz(fitted_moves, optimized_movements) * amino_acid_distance
    xyz = pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])
    xyz = pd.concat([ca_trace[['ID', 'Amino Acid']], xyz], axis=1)

    untilted_xyz = convert_to_xyz(fitted_moves, movements)
    untilted_xyz = pd.DataFrame(untilted_xyz, columns=['X', 'Y', 'Z'])
    untilted_xyz = pd.concat([ca_trace[['ID', 'Amino Acid']], untilted_xyz], axis=1)

    print('-' * 50)
    print(f"Total Cost: {structure_cost + fitted_cost}")
    print(f"Total Time: {tilt_time + fitted_time}")
    print('-' * 50)

    return xyz, untilted_xyz


def get_movements(num_moves):
    """
    Get the name and movements for a given number of moves.
    :param num_moves:
    :return: structure_name, movements
    """

    # Define Math Calculations
    sqrt_3_div_2 = np.sqrt(3) / 2
    sqrt_2_div_2 = np.sqrt(2) / 2

    # Return Structure Name and Movements
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
        return ("TRIANGULAR PRISMATIC HONEYCOMB",
                [
                    [sqrt_3_div_2, 0.5, 0], [-sqrt_3_div_2, 0.5, 0],
                    [0, 1, 0], [sqrt_3_div_2, -0.5, 0],
                    [-sqrt_3_div_2, -0.5, 0], [0, -1, 0],
                    [0, 0, 1], [0, 0, -1]
                ])
    elif num_moves == 12:
        return ("TETRAHEDRAL-OCTAHEDRAL HONEYCOMB",
                [
                    [sqrt_2_div_2, sqrt_2_div_2, 0], [sqrt_2_div_2, 0, sqrt_2_div_2],
                    [0, sqrt_2_div_2, sqrt_2_div_2], [-sqrt_2_div_2, -sqrt_2_div_2, 0],
                    [-sqrt_2_div_2, 0, -sqrt_2_div_2], [0, -sqrt_2_div_2, -sqrt_2_div_2],
                    [sqrt_2_div_2, -sqrt_2_div_2, 0], [sqrt_2_div_2, 0, -sqrt_2_div_2],
                    [0, sqrt_2_div_2, -sqrt_2_div_2], [-sqrt_2_div_2, sqrt_2_div_2, 0],
                    [-sqrt_2_div_2, 0, sqrt_2_div_2], [0, -sqrt_2_div_2, sqrt_2_div_2]
                ])


def convert_to_xyz(moves, possible_movements):
    """
    Convert a list of moves to a list of XYZ coordinates
    :param moves:
    :param possible_movements:
    :return: xyz
    """

    # Ensure moves is a NumPy array
    moves = np.array(moves, dtype=int)

    # Check if possible_movements is a list of lists or a 2D NumPy array
    if isinstance(possible_movements, list):
        possible_movements = np.array(possible_movements)

    # Initialize the xyz array with the origin and correct size
    xyz = np.zeros((len(moves) + 1, 3), dtype=np.float16)

    # Efficiently compute the cumulative sum of movements
    xyz[1:] = np.cumsum(possible_movements[moves], axis=0, dtype=np.float16)

    return xyz


def get_amino_acid_distance(xyz):
    """
    Get the average distance between amino acids
    :param xyz:
    :return: average_distance
    """

    # Get the distance between amino acids
    amino_acid_distance = 0
    for i in range(len(xyz) - 1):
        amino_acid_distance += np.linalg.norm(xyz.iloc[i] - xyz.iloc[i + 1])

    return amino_acid_distance / (len(xyz) - 1)
