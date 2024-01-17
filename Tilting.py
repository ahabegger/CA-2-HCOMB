import numpy as np

'''
Tilting.py
Defines functions for optimizing the tilt of a given set of movements with respect 
to a backbone structure defined by XYZ coordinates. The primary function, `optimize_tilt`, 
iteratively rotates the movements in 3D space, evaluating each rotation using a cost function 
to find the combination of movements that minimizes the cost. Auxiliary functions 
`rotate_movements`, `create_cost_matrix`, and `get_cost` support this process by handling 
the rotation calculations, creating a cost matrix, and calculating the cost of movements, 
respectively.
'''


def optimize_tilt(backbone_xyz, movements):
    backbone_xyz_np = backbone_xyz[['X', 'Y', 'Z']].to_numpy()
    lowest_sum = get_cost(backbone_xyz_np, movements)
    lowest_movements = movements

    x, y, z = 0, 0, 0

    for i in np.arange(0, 375, 10):
        for j in np.arange(0, 375, 10):
            for k in np.arange(0, 375, 10):
                if 0 <= i <= 360 and 0 <= j <= 360 and 0 <= k <= 360:
                    tilt_movements = rotate_movements(movements, i, j, k)
                    current_sum = get_cost(backbone_xyz_np, tilt_movements)
                    if current_sum < lowest_sum:
                        lowest_sum = current_sum
                        lowest_movements = tilt_movements
                        x, y, z = i, j, k

    for i in np.arange(x - 10, x + 10):
        for j in np.arange(y - 10, y + 10):
            for k in np.arange(z - 10, z + 10):
                if 0 <= i <= 360 and 0 <= j <= 360 and 0 <= k <= 360:
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

    # Compute sin and cos for each angle
    sin_x, cos_x = np.sin(angles_rad_x), np.cos(angles_rad_x)
    sin_y, cos_y = np.sin(angles_rad_y), np.cos(angles_rad_y)
    sin_z, cos_z = np.sin(angles_rad_z), np.cos(angles_rad_z)

    # Directly compute the combined rotation matrix
    rotation_matrix = np.array([
        [cos_y * cos_z, cos_z * sin_x * sin_y - cos_x * sin_z, sin_x * sin_z + cos_x * cos_z * sin_y],
        [cos_y * sin_z, cos_x * cos_z + sin_x * sin_y * sin_z, cos_x * sin_y * sin_z - cos_z * sin_x],
        [-sin_y, cos_y * sin_x, cos_x * cos_y]
    ])

    # Apply the rotation to the movements
    changed_movements = np.dot(movements, rotation_matrix)

    return changed_movements


def create_cost_matrix(backbone_xyz_np, movements):
    # Compute movement vectors and their magnitudes
    movement_vectors = backbone_xyz_np[1:] - backbone_xyz_np[:-1]
    magnitudes = np.linalg.norm(movement_vectors, axis=1)

    # Initialize the cost matrix
    cost_matrix = np.zeros((movement_vectors.shape[0], len(movements)), dtype=np.float16)

    # Iterate over movements to calculate costs
    for i, movement in enumerate(movements):
        # Convert movement to float32
        movement = np.array(movement, dtype=np.float16)

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
