import pandas as pd
from Bio import PDB
import urllib.request

'''
This script will take a PDB file and convert it into a backbone-only XYZ.
'''


def create_backbone(pdb_id):
    # Define the URL for the PDB file
    pdb_url = f'https://files.rcsb.org/download/{pdb_id}.pdb'

    try:
        # Download the PDB file
        pdb_file, _ = urllib.request.urlretrieve(pdb_url, f'{pdb_id}.pdb')

        # Initialize a PDB parser
        parser = PDB.PDBParser(QUIET=True)

        # Parse the PDB file
        structure = parser.get_structure(pdb_id, pdb_file)

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


if __name__ == "__main__":
    # Example usage:
    pdb_code = "2WFU"  # Replace with the PDB code you want to analyze
    df = create_backbone(pdb_code)
    print(df)
