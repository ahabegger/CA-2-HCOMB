import pandas as pd
import GenerateOutput.GenerateDiagram as diagrams
import GenerateOutput.GeneratePDB as pdb
from PDB2Backbone import create_backbone

'''
GenerateReport.py
This Script takes a PDB code and a DataFrame containing the new coordinates of the protein backbone and creates a
report containing the original PDB file, the modified PDB file, and the diagrams of both.
'''


def create_report(pdb_code, output_xyz, structure):
    # Download the PDB file
    pdb.download_pdb(pdb_code)

    # Create the Modified PDB File
    pdb.create_modified_pdb(pdb_code, output_xyz, structure)

    # Create the Diagrams
    diagrams.create_nglview(f"GenerateOutput/PDB_Files/{pdb_code}.pdb")
    diagrams.create_nglview(f"GenerateOutput/PDB_Files/{pdb_code}_modified.pdb")

    # Create the Report
    write_report_html(pdb_code, structure, output_xyz)


def write_report_html(pdb_code, structure, xyz):
    input_diagram_file = f"{pdb_code}_diagram.html"
    output_diagram_file = f"{pdb_code}_modified_diagram.html"
    input_diagram = diagrams.get_nglview_html(input_diagram_file)
    output_diagram = diagrams.get_nglview_html(output_diagram_file)

    pdb_url = f'https://files.rcsb.org/download/{pdb_code}.pdb'

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
          f"<h2>{pdb_code} Changed to {structure} Structure</h2>\n" \
          f"<h3>Input Model</h3>\n" \
          f"<p>TransformationReports/PDB_Files/{pdb_code}.pdb</p>\n" \
          f"<p>Download Here : <a href=\"{pdb_url}\">{pdb_code}.pdb</a></p>\n"

    bottom = '</body>\n<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" ' \
             'integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" ' \
             'crossorigin="anonymous"></script>\n</html> '

    intermediate = f'<h3>Intermediate Model</h3>\n'

    backbone = create_backbone(f"GenerateOutput/PDB_Files/{pdb_code}.pdb")
    plot_filename = f"GenerateOutput/Reports/Plots/{pdb_code}_backbone.png"
    backbone_plot = diagrams.plot_structure_to_image(backbone[['X', 'Y', 'Z']],
                                                     plot_filename,
                                                     title="CA Backbone Structure")

    middle = f'<h3>Output Model</h3>\n' \
             f'<p>GenerateOutput/PDB_Files/{pdb_code}_modified.pdb</p>\n'

    # Replace spaces and - with underscores
    structure = structure.replace(' ', '_').replace('-', '_')

    plot_filename = f"GenerateOutput/Reports/Plots/{pdb_code}_{structure}.png"
    output_plot = diagrams.plot_structure_to_image(xyz,
                                                   plot_filename,
                                                   title=f"{structure} Structure")
    output_diagram = output_plot + output_diagram

    compare = f'<h3>Comparison XYZ</h3>\n'
    backbone = start_at_zero(backbone)
    backbone = backbone.rename(columns={'X': 'Backbone_X', 'Y': 'Backbone_Y', 'Z': 'Backbone_Z'})
    xyz = xyz.rename(columns={'X': 'Output_X', 'Y': f'Output_Y', 'Z': f'Output_Z'})
    xyz = xyz.drop(columns=['ID', 'Amino Acid'])
    combined_df = pd.concat([backbone, xyz], axis=1)
    combined_table = combined_df.to_html()

    html = (top + input_diagram + intermediate + backbone_plot + middle +
            output_diagram + compare + combined_table + bottom)

    with open(f"GenerateOutput/Reports/{pdb_code}_{structure.replace(' ', '_')}.html", 'w') as file:
        file.write(html)


def start_at_zero(df):
    for col in ['X', 'Y', 'Z']:
        if col in df.columns:
            original_first_value = df[col].iloc[0]
            df[col] = df[col] - original_first_value
    return df
