"""
Performance.py
"""
import os

import numpy as np


def calculate_tm_align(template_pdb, modified_pdb):
    """
    Calculate the TM-Align score between two PDB files.
    :param template_pdb:
    :param modified_pdb:
    :return:
    """
    # Run TM-Align
    os.system(f".\TM-Align\TMalign {template_pdb} {modified_pdb} > TM-Align_Output.txt")

    # Read the TM-Align output file
    with open("TM-Align_Output.txt", 'r') as file:
        tm_score = float(file.readlines()[21].split()[1])

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
