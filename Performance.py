"""
Performance.py
To calculate the TM-Align score and Root-Mean-Square Deviation (RMSD)
between two sets of xyz coordinates.
"""

import tmtools
import numpy as np

"""
tmtools is a Python package that provides a wrapper for the TM-Align executable. It allows you to use TM-Align in 
your Python code.TM-Align Algorithm has been developed by Dr. Yang Zhang and his team: 
Y. Zhang, J. Skolnick, 
Scoring function for automated assessment of protein structure template quality, Proteins, 57: 702-710 (2004). 
J. Xu, Y. Zhang, 
How significant is a protein structure similarity with TM-score=0.5? Bioinformatics, 26, 889-895 (2010).
"""


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
    tm_results = tmtools.tm_align(template_xyz, modified_xyz, sequence, sequence)

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


def calculate_rnm_score(template_xyz, modified_xyz):
    """
    Calculate the RNM-Align score between two sets of xyz coordinates.
    :param template_xyz: Numpy array of xyz coordinates for the template
    :param modified_xyz: Numpy array of xyz coordinates for the modified structure
    :return: rnm_score
    """

    n = template_xyz.shape[0]
    total = 0

    for i in range(n-1):
        template_m = template_xyz[i+1] - template_xyz[i]
        template_norm = np.linalg.norm(template_m)
        template_m = template_m / template_norm
        modified_m = modified_xyz[i+1] - modified_xyz[i]
        modified_norm = np.linalg.norm(modified_m)
        modified_m = modified_m / modified_norm
        dot_product = np.dot(template_m, modified_m)

        # Ensure the dot product is clamped between -1 and 1 for the arccos function
        dot_product_clamped = np.clip(dot_product, -1.0, 1.0)

        angle = np.arccos(dot_product_clamped)
        total += angle

    rnm_score_radians = (1 / (n-1)) * total
    rnm_score_degrees = rnm_score_radians * (180 / np.pi)

    return rnm_score_radians, rnm_score_degrees


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
