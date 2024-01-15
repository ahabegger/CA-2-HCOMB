import time
import numpy as np
import pandas as pd


def optimize_tilt(backbone_xyz, movements):
    backbone_xyz_np = backbone_xyz[['X', 'Y', 'Z']].to_numpy()
    lowest_sum = get_cost(backbone_xyz_np, movements)
    lowest_movements = movements

    x, y, z = 0, 0, 0

    for i in range(0, 360, 15):
        for j in range(0, 360, 15):
            for k in range(0, 360, 15):
                tilt_movements = rotate_movements(movements, i, j, k)
                current_sum = get_cost(backbone_xyz_np, tilt_movements)
                if current_sum < lowest_sum:
                    lowest_sum = current_sum
                    lowest_movements = tilt_movements
                    x, y, z = i, j, k

    for i in range(x - 15, x + 15):
        for j in range(y - 15, y + 15):
            for k in range(z - 15, z + 15):
                tilt_movements = rotate_movements(movements, i, j, k)
                current_sum = get_cost(backbone_xyz_np, tilt_movements)
                if current_sum < lowest_sum:
                    lowest_sum = current_sum
                    lowest_movements = tilt_movements
                    x, y, z = i, j, k

    # Create normalized cost matrix
    cost_matrix = create_cost_matrix(backbone_xyz_np, lowest_movements)

    return lowest_movements, cost_matrix, lowest_sum, [x, y, z]


def rotate_movements(movements, degree_x, degree_y, degree_z):
    # Convert degrees to radians
    angles_rad_x = np.radians(degree_x)
    angles_rad_y = np.radians(degree_y)
    angles_rad_z = np.radians(degree_z)

    # Create rotation matrices for each axis
    cos_x, sin_x = np.cos(angles_rad_x), np.sin(angles_rad_x)
    rotation_matrix_x = np.array([[1, 0, 0],
                                  [0, cos_x, -sin_x],
                                  [0, sin_x, cos_x]])

    cos_y, sin_y = np.cos(angles_rad_y), np.sin(angles_rad_y)
    rotation_matrix_y = np.array([[cos_y, 0, sin_y],
                                  [0, 1, 0],
                                  [-sin_y, 0, cos_y]])

    cos_z, sin_z = np.cos(angles_rad_z), np.sin(angles_rad_z)
    rotation_matrix_z = np.array([[cos_z, -sin_z, 0],
                                  [sin_z, cos_z, 0],
                                  [0, 0, 1]])

    # Combined rotation matrix
    combined_rotation_matrix = np.dot(np.dot(rotation_matrix_z, rotation_matrix_y), rotation_matrix_x)
    changed_movements = np.dot(movements, combined_rotation_matrix)

    return changed_movements


def create_cost_matrix(backbone_xyz_np, movements):
    # Compute movement vectors and their magnitudes
    movement_vectors = backbone_xyz_np[1:] - backbone_xyz_np[:-1]
    magnitudes = np.linalg.norm(movement_vectors, axis=1)

    # Initialize the cost matrix
    cost_matrix = np.zeros((movement_vectors.shape[0], len(movements)))

    # Iterate over movements to calculate costs
    for i, movement in enumerate(movements):
        # Normalize movement vectors and compute the cost
        # Handle zero magnitudes to avoid division by zero
        norm_movement_vectors = movement_vectors / magnitudes[:, np.newaxis]
        norm_movement_vectors[magnitudes == 0] = 0
        cost_matrix[:, i] = np.linalg.norm(norm_movement_vectors - movement, axis=1)

    # Find the minimum value in each row
    lowest_costs = np.min(cost_matrix, axis=1)

    # Subtract the minimum value from each element in the row
    cost_matrix = cost_matrix - lowest_costs[:, np.newaxis]

    return cost_matrix


def get_cost(backbone_xyz_np, movements):
    # Compute movement vectors and their magnitudes
    movement_vectors = backbone_xyz_np[1:] - backbone_xyz_np[:-1]
    magnitudes = np.linalg.norm(movement_vectors, axis=1)

    # Initialize the cost matrix
    cost_matrix = np.zeros((movement_vectors.shape[0], len(movements)))

    # Iterate over movements to calculate costs
    for i, movement in enumerate(movements):
        # Normalize movement vectors and compute the cost
        # Handle zero magnitudes to avoid division by zero
        norm_movement_vectors = movement_vectors / magnitudes[:, np.newaxis]
        norm_movement_vectors[magnitudes == 0] = 0
        cost_matrix[:, i] = np.linalg.norm(norm_movement_vectors - movement, axis=1)

    # Return the sum of minimum costs for each vector
    return np.min(cost_matrix, axis=1).sum()

