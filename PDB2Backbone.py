"""
PDB2Backbone.py
Parse a given PDB (Protein Data Bank) file and extract the backbone structure of
a protein. It focuses on creating a DataFrame containing the amino acid sequence
and the corresponding X, Y, Z coordinates of each alpha carbon (CA) atom in the
protein's backbone, thus providing a structural representation of the protein for
further analysis or manipulation.
"""

import pandas as pd
from Bio import PDB


def create_backbone(pdb_filepath):
    """
    Create a DataFrame containing the amino acid sequence and the corresponding X, Y, Z
    :param pdb_filepath:
    :return: xyz_df
    """

    # Initialize a PDB parser
    parser = PDB.PDBParser(QUIET=True)

    # Parse the PDB file and PDB ID
    pdb_id = pdb_filepath.split('/')[-1].split('.')[0]
    structure = parser.get_structure(pdb_id, pdb_filepath)

    # Create lists to store data
    chain_id = []
    amino_acids = []
    coordinates = [[], [], []]  # X, Y, Z

    # Iterate over all models, chains, residues, and atoms
    for model in structure:
        for chain in model:
            for residue in chain:
                residue_name = residue.get_resname()
                for atom in residue:
                    if atom.name == "CA":
                        chain_id.append(f"{chain.id}:{residue.id[1]}")
                        amino_acids.append(residue_name)
                        coordinates[0].append(atom.get_coord()[0])  # X
                        coordinates[1].append(atom.get_coord()[1])  # Y
                        coordinates[2].append(atom.get_coord()[2])  # Z

    # Create a DataFrame
    xyz_df = pd.DataFrame({'ID': chain_id,
                           'Amino Acid': amino_acids,
                           'X': coordinates[0],
                           'Y': coordinates[1],
                           'Z': coordinates[2]})

    return xyz_df
