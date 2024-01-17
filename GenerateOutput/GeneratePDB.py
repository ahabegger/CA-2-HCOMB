import os
import urllib.request
import requests

'''
GeneratePDB.py
This Script takes a PDB code and a DataFrame containing the new coordinates of the protein backbone and creates a
report containing the original PDB file, the modified PDB file, and the diagrams of both.
'''


def download_pdb(pdb_id):
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    response = requests.get(url)

    # If the request was successful
    if response.status_code == 200:
        file_path = f'TransformationReports/PDB_Files/{pdb_id}.pdb'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True
    else:
        print(f'Error downloading {pdb_id}.pdb. Status code: {response.status_code}')
        return False


def create_modified_pdb(pdb_code, output_xyz, structure):
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
    # Ensure the new coordinates are in the correct format
    return (input_line[:30] +
            f"{new_coords.X:8.3f}" +  # New X coordinate
            f"{new_coords.Y:8.3f}" +  # New Y coordinate
            f"{new_coords.Z:8.3f}" +  # New Z coordinate
            input_line[54:])
