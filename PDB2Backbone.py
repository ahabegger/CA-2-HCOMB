import requests
import pandas as pd
from Bio import PDB
import urllib.request

'''
This script will take a PDB file and convert it into a backbone-only XYZ.
'''


def create_backbone(pdb_code):
    # Define the URL for the PDB file
    pdb_url = f'https://files.rcsb.org/download/{pdb_code}.pdb'

    try:
        # Download the PDB file
        pdb_file, _ = urllib.request.urlretrieve(pdb_url, f'{pdb_code}.pdb')

        # Initialize a PDB parser
        parser = PDB.PDBParser(QUIET=True)

        # Parse the PDB file
        structure = parser.get_structure(pdb_code, pdb_file)

        # Create lists to store data
        id = []
        amino_acids = []
        coordinates = [[], [], []]

        # Iterate over all models, chains, residues, and atoms
        for model in structure:
            for chain in model:
                for residue in chain:
                    resname = residue.get_resname()
                    for atom in residue:
                        if atom.name == "CA":
                            id.append(f"{chain.id}:{residue.id[1]}")
                            amino_acids.append(resname)
                            coordinates[0].append(atom.get_coord()[0])  # X
                            coordinates[1].append(atom.get_coord()[1])  # Y
                            coordinates[2].append(atom.get_coord()[2])  # Z

        # Create a DataFrame
        df = pd.DataFrame({'ID': id,
                           'Amino Acid': amino_acids,
                           'X': coordinates[0],
                           'Y': coordinates[1],
                           'Z': coordinates[2]})

        return df

    except Exception as e:
        return f"Error: {str(e)}"


def download_pdb(pdb_id):
    # Construct the URL
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'

    # Send a request to the URL
    response = requests.get(url)

    # If the request was successful
    if response.status_code == 200:
        return response.content
    else:
        print(f'Error downloading {pdb_id}.pdb. Status code: {response.status_code}')
        exit(0)


class Structure:
    def __init__(self, model, nonstandard):
        included_lines = ["ATOM"]

        self.atom_lines = ''
        self.seq_lines = ''
        start = 1

        if nonstandard:
            included_lines.append("HETATM")

        for line in model.splitlines():
            if line.split()[0] in included_lines:
                if line.split()[2] in ['CA']:
                    self.atom_lines += f"{line[:7]}{start:>4}{line[11:]}" + '\n'
                    start += 1
            elif line.split()[0] in ["SEQRES"]:
                self.seq_lines += line + '\n'

        self.input_xyz = self.parse_xyz()
        self.output_xyz = self.input_xyz

    def parse_xyz(self):
        xyz_array = []

        for line in self.atom_lines.splitlines():
            coordinates = line.split()
            xyz_array.append([float(coordinates[6]), float(coordinates[7]), float(coordinates[8])])

        return xyz_array

    def replace_xyz(self):
        new_atom_lines = ''
        split_lines = self.atom_lines.splitlines()
        for x in range(len(split_lines)):
            print(split_lines[x])
            replace_line = self.replace_coordinates(split_lines[x], self.output_xyz[x])
            print(replace_line)
            new_atom_lines += replace_line + '\n'

        return new_atom_lines

    def replace_coordinates(self, atom_line, new_coords):
        # Ensure the new coordinates are in the correct format (right-aligned within 8 characters)
        formatted_coords = [f"{coord:8.3f}" for coord in new_coords]

        # Replace the coordinates in the line
        new_line = (
                atom_line[:30] +  # Everything before the X coordinate
                formatted_coords[0] +  # New X coordinate
                formatted_coords[1] +  # New Y coordinate
                formatted_coords[2] +  # New Z coordinate
                atom_line[54:]  # Everything after the Z coordinate
        )

        return new_line

    def print(self):
        print(self.seq_lines)
        print(self.atom_lines)
        print(self.input_xyz)
        print(self.output_xyz)


if __name__ == "__main__":
    # Example usage:
    pdb_code = "2WFU"  # Replace with the PDB code you want to analyze
    df = create_backbone(pdb_code)
    print(df)
