import requests
import nglview
import os

'''
GenerateReport.py
This Script takes a PDB code and a DataFrame containing the new coordinates of the protein backbone and creates a
report containing the original PDB file, the modified PDB file, and the diagrams of both.
'''


def create_report(pdb_code, output_xyz, structure):
    # Download the PDB file
    download_pdb(pdb_code)

    # Create the Modified PDB File
    create_modified_pdb(pdb_code, output_xyz, structure)

    # Create the Diagrams
    create_diagram(f"TransformationReports/PDB_Files/{pdb_code}.pdb")
    create_diagram(f"TransformationReports/PDB_Files/{pdb_code}_modified.pdb")

    # Create the Report
    write_report_html(pdb_code, structure)


def write_report_html(pdb_code, structure):
    input_diagram = ""
    with open(f"{pdb_code}_diagram.html") as file:
        for line in file:
            input_diagram += line
    input_diagram = input_diagram.split("body>")[1][:-2]
    os.remove(f"{pdb_code}_diagram.html")

    output_diagram = ""
    with open(f"{pdb_code}_modified_diagram.html") as file:
        for line in file:
            output_diagram += line
    output_diagram = output_diagram.split("body>")[1][:-2]
    os.remove(f"{pdb_code}_modified_diagram.html")

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
          f"<h2>{pdb_code} Changed to {structure}</h2>\n" \
          f"<h3>Input Model</h3>\n" \
          f"TransformationReports/PDB_Files/{pdb_code}.pdb\n"

    bottom = '</body>\n<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" ' \
             'integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" ' \
             'crossorigin="anonymous"></script>\n</html> '

    middle = f'<h3>Output Model</h3>\n' \
             f'TransformationReports/PDB_Files/{pdb_code}_modified.pdb\n'

    html = top + input_diagram + middle + output_diagram + bottom
    with open(f"TransformationReports/Reports/{pdb_code}_transformation.html", 'w') as file:
        file.write(html)


def create_diagram(pdb_file):
    view = nglview.show_structure_file(pdb_file)
    nglview.write_html(f'{pdb_file.split("/")[2].split(".")[0]}_diagram.html', view)


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


if __name__ == "__main__":
    pass
