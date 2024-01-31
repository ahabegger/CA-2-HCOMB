"""
Performance.py
"""

import numpy as np


def calculate_tm_align():
    tm_score = 0
    return tm_score


def calculate_rmsd(template_ca_xyz, target_ca_xyz):
    """
    Calculate the Root-Mean-Square Deviation (RMSD) between two sets of points.

    :param template_ca_xyz: Numpy array of xyz coordinates for the template
    :param target_ca_xyz: Numpy array of xyz coordinates for the target
    :return: rmsd value
    """
    if template_ca_xyz.shape != target_ca_xyz.shape:
        raise ValueError("The input arrays must have the same shape.")

    # Calculate the squared differences
    diff_squared = np.square(template_ca_xyz - target_ca_xyz)

    # Compute the mean of the squared differences
    mean_diff_squared = np.mean(diff_squared)

    # Calculate the square root of the mean
    rmsd = np.sqrt(mean_diff_squared)

    return rmsd

