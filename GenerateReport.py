import requests
import nglview
import numpy as np
import pandas as pd


def create_report(pdb_code, output_xyz, structure):
    # Download the PDB file
    download_pdb(pdb_code)

    # Create the Modified PDB File
    create_modified_pdb(pdb_code, output_xyz, structure)


def pause(pdb_code):
    input_diagram = ""
    with open(f"diagram_{pdb_code}.html") as file:
        for line in file:
            input_diagram += line
    input_diagram = input_diagram.split("body>")[1][:-2]

    output_diagram = ""
    with open(f"diagram_{pdb_code}_modified.html") as file:
        for line in file:
            output_diagram += line
    output_diagram = output_diagram.split("body>")[1][:-2]

    changes = ""
    with open(f"Modified_PDB_Files/{pdb_code}_modified.pdb") as file:
        for line in file:
            if "REMARK" in line:
                changes += '<p>' + line + '</p>\n'

    top = f"<!DOCTYPE html>\n" \
          f"<html lang=\"en\">\n" \
          f"<head>\n" \
          f"   <meta charset=\"UTF-8\">\n" \
          f"   <title>{pdb_code} Transformation</title>\n" \
          f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" ' \
          f'integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" ' \
          f'crossorigin="anonymous">\n' \
          f"</head>\n" \
          f"<body>\n" \
          f"<h1>PDB2LatticePy Report</h1>\n" \
          f"<h2>{pdb_code} M2M Transformation</h2>\n"
    for part in title.replace('TITLE', '').split('\n'):
        top += f"<h2>{part}</h2>\n"
    top += f"<h3>Input Model</h3>\n"

    bottom = '</body>\n<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" ' \
             'integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" ' \
             'crossorigin="anonymous"></script>\n</html> '

    middle = '<h3>Changes</h3>\n' \
             f'{changes.replace("REMARK", "")}\n' \
             '<h3>Output Model</h3>\n'

    code = top + input_diagram + middle + output_diagram + bottom
    with open(f"Reports/{pdb_code}_transformation.html", 'w') as file:
        file.write(code)


def view_pdb(pdb_file):
    view = nglview.show_structure_file(pdb_file)
    nglview.write_html(f'Diagrams/{pdb_file.split("/")[1].split(".")[0]}.html', view)
    return view


def download_pdb(pdb_id):
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'

    # Send a request to the URL
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


def replace_coordinates(input_line, new_coords):
    # Ensure the new coordinates are in the correct format
    return (input_line[:30] +
            f"{new_coords.X:8.3f}" +  # New X coordinate
            f"{new_coords.Y:8.3f}" +  # New Y coordinate
            f"{new_coords.Z:8.3f}" +  # New Z coordinate
            input_line[54:])


def create_modified_pdb(pdb_code, output_xyz, structure):
    # Set the PDB file structure
    header = f"HEADER    Modified File of {pdb_code}"
    title = f"TITLE     {structure} {pdb_code}"
    remark = (f"REMARK    All Credit to the original authors of {pdb_code}\n"
              f"REMARK    Changed using PDB2LatticePy\n"
              f"REMARK    GitHub: https://github.com/ahabegger/PDB-2-Lattice")
    seq_lines = ""
    atom_lines = ""
    end = "END"

    # Read the PDB file
    with open(f"TransformationReports/PDB_Files/{pdb_code}.pdb") as file:
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
    with open(f"TransformationReports/PDB_Files/{pdb_code}_modified.pdb", 'w') as file:
        file.write(header + '\n')
        file.write(title + '\n')
        file.write(remark + '\n')
        file.write(seq_lines)
        for x in range(len(atom_lines.splitlines())):
            new_line = replace_coordinates(atom_lines.splitlines()[x], output_xyz.iloc[x])
            file.write(new_line + '\n')
        file.write(end)


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
    pass
