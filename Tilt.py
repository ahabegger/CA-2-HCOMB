import numpy as np
import math


def rotate_movements(movements, degree_x, degree_y, degree_z):
    # Convert degrees to radians
    angle_rad_x = math.radians(degree_x)
    angle_rad_y = math.radians(degree_y)
    angle_rad_z = math.radians(degree_z)

    # Rotation matrix for X-axis
    rotation_matrix_x = np.array([[1, 0, 0],
                                  [0, np.cos(angle_rad_x), -np.sin(angle_rad_x)],
                                  [0, np.sin(angle_rad_x), np.cos(angle_rad_x)]])

    # Rotation matrix for Y-axis
    rotation_matrix_y = np.array([[np.cos(angle_rad_y), 0, np.sin(angle_rad_y)],
                                  [0, 1, 0],
                                  [-np.sin(angle_rad_y), 0, np.cos(angle_rad_y)]])

    # Rotation matrix for Z-axis
    rotation_matrix_z = np.array([[np.cos(angle_rad_z), -np.sin(angle_rad_z), 0],
                                  [np.sin(angle_rad_z), np.cos(angle_rad_z), 0],
                                  [0, 0, 1]])

    # Combined rotation matrix
    combined_rotation_matrix = np.dot(np.dot(rotation_matrix_z, rotation_matrix_y), rotation_matrix_x)
    changed_movements = np.dot(movements, combined_rotation_matrix)

    return changed_movements


# Example usage:
if __name__ == "__main__":
    pass
