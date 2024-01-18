"""
GeneratePDB.py
Facilitate the validation, downloading, and manipulation of PDB (Protein Data Bank) files.
Key functions include checking the validity of a given PDB ID, downloading PDB files,
counting the number of chains in a PDB file, and creating a modified PDB file with new
XYZ coordinates, which is essential for protein structure analysis and visualization.
"""

import os
import urllib.request
import requests


def check_pdb_is_valid(pdb_id):
    """
    Check if the given PDB ID is valid.
    :param pdb_id:
    :return: validity
    """

    # Define the URL for the PDB file
    pdb_url = f'https://files.rcsb.org/download/{pdb_id}.pdb'

    try:
        # Download the PDB file
        pdb_file, _ = urllib.request.urlretrieve(pdb_url, f'{pdb_id}.pdb')

        # Remove the PDB file
        os.remove(f'{pdb_id}.pdb')

        return True

    except Exception as e:
        print(f'Not a valid PDB code: {pdb_id}.')
        print(f'Error: {e}')
        return False


def download_pdb(pdb_id):
    """
    Download the PDB file for the given PDB ID.
    :param pdb_id:
    :return:
    """

    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    response = requests.get(url)

    # If the request was successful
    if response.status_code == 200:
        file_path = f'GenerateOutput/PDB_Files/{pdb_id}.pdb'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    else:
        print(f'Error downloading {pdb_id}.pdb. Status code: {response.status_code}')


def count_chains_in_pdb(pdb_code):
    """
    Count the number of chains in the given PDB file.
    :param pdb_code:
    :return: chain_count
    """

    chain_ids = set()
    pdb_filepath = f"GenerateOutput/PDB_Files/{pdb_code}.pdb"

    try:
        with open(pdb_filepath, 'r') as file:
            for line in file:
                if line.startswith("ATOM"):
                    chain_id = line[21]  # Chain ID is located at index 21
                    chain_ids.add(chain_id)
    except FileNotFoundError:
        print(f"File not found: {pdb_filepath}")
        return 0

    return len(chain_ids)


def create_modified_pdb(pdb_code, output_xyz, structure):
    """
    Creates a PDB file for the new Structure
    :param pdb_code:
    :param output_xyz:
    :param structure:
    :return:
    """

    # Set the PDB file structure
    header = f"HEADER    Modified File of {pdb_code}"
    title = f"TITLE     {structure} {pdb_code}"
    remark = (f"REMARK    All Credit to the original authors of {pdb_code}\n"
              f"REMARK    Changed using PDB2Lattice\n"
              f"REMARK    GitHub: https://github.com/ahabegger/PDB-2-Lattice")
    seq_lines = ""
    atom_lines = ""
    end = "END"

    # Read the PDB file
    with open(f"GenerateOutput/PDB_Files/{pdb_code}.pdb") as file:
        pdb_file = file.read()
        counter = 1
        for line in pdb_file.splitlines():
            # Add the SEQRES lines to the new PDB file
            if line.split()[0] == "SEQRES":
                seq_lines += line + '\n'

            # Add the ATOM lines to the new PDB file
            if line.split()[0] in ["ATOM"]:
                if line.split()[2] in ['CA']:
                    atom_lines += f"{line[:7]}{counter:>4}{line[11:]}" + '\n'
                    counter += 1

    # Create the new Modified PDB file
    with open(f"GenerateOutput/PDB_Files/{pdb_code}_modified.pdb", 'w') as file:
        file.write(header + '\n')
        file.write(title + '\n')
        file.write(remark + '\n')
        file.write(seq_lines)
        for x in range(len(atom_lines.splitlines())):
            new_line = replace_coordinates(atom_lines.splitlines()[x], output_xyz.iloc[x])
            file.write(new_line + '\n')
        file.write(end)


def replace_coordinates(input_line, new_coords):
    """
    Replace the coordinates in the given line with the new coordinates.
    :param input_line:
    :param new_coords:
    :return: new_line
    """

    # Ensure the new coordinates are in the correct format
    return (input_line[:30] +
            f"{new_coords.X:8.3f}" +  # New X coordinate
            f"{new_coords.Y:8.3f}" +  # New Y coordinate
            f"{new_coords.Z:8.3f}" +  # New Z coordinate
            input_line[54:])
