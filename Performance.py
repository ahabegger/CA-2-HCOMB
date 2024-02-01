"""
Performance.py
To calculate the TM-Align score and Root-Mean-Square Deviation (RMSD)
between two sets of xyz coordinates.
"""

from tmtools import tm_align
import numpy as np


def calculate_tm_score(template_xyz, modified_xyz, amino_acids):
    """
    Calculate the TM-Align score between two sets of xyz coordinates.

    :param amino_acids: Amino acids in the structure
    :param template_xyz: Numpy array of xyz coordinates for the template
    :param modified_xyz: Numpy array of xyz coordinates for the modified structure
    :return: tm_score
    """

    # Convert the amino acids to a string
    sequence = ''
    amino_acids.tolist()
    for acid in amino_acids:
        sequence += three_letter_amino_acid_to_one_letter(acid)

    # Calculate the TM-Align score
    tm_results = tm_align(template_xyz, modified_xyz, sequence, sequence)

    # Get the TM-Align score
    # tm_norm_chain1 is the TM-score normalized by the length of the first chain
    # (or the template structure). This score tells you how well the second chain
    # (or the modified structure) aligns with the template.
    tm_score = tm_results.tm_norm_chain1

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


def three_letter_amino_acid_to_one_letter(three_letter):
    """
    Convert a three-letter amino acid code to a one-letter code.
    :param three_letter: string
    :return: one_letter: string
    """
    one_letter = {
        "ALA": "A",
        "ARG": "R",
        "ASN": "N",
        "ASP": "D",
        "CYS": "C",
        "GLN": "Q",
        "GLU": "E",
        "GLY": "G",
        "HIS": "H",
        "ILE": "I",
        "LEU": "L",
        "LYS": "K",
        "MET": "M",
        "PHE": "F",
        "PRO": "P",
        "SER": "S",
        "THR": "T",
        "TRP": "W",
        "TYR": "Y",
        "VAL": "V"
    }

    return one_letter.get(three_letter, "X")
