import argparse
import os
import pandas as pd
from GenerateOutput.GenerateDiagram import plot_structure
from GenerateOutput.GeneratePDB import create_modified_pdb, download_pdb, check_pdb_is_valid, count_chains_in_pdb
from GenerateOutput.GenerateReport import create_report
from PDB2Backbone import create_backbone
from Structures import create_structure

'''
main.py
To process protein structures from PDB (Protein Data Bank) files or IDs, and convert them into 
simplified structural representations based on specified parameters. The script offers functionalities 
like creating different structural models (e.g., CA Backbone, Cubic Honeycomb), generating reports, 
visualizing structures, and exporting results in XYZ or PDB formats, while also handling user 
input and command-line arguments to tailor the processing to specific needs.
'''


def execute(pdb_id, pdb_file, structure_num, visualize_toggle,
            report_toggle, output_xyz_file, output_pdb_file,
            multiprocess_toggle, no_footprint_toggle):
    structure_num = int(structure_num)
    structure_name = {
        1: "CA Backbone",
        4: "Square Tiling",
        6: "Cubic Honeycomb",
        8: "Triangular Prismatic Honeycomb",
        12: "Tetrahedral-Octahedral Honeycomb"
    }

    if structure_num == 1:  # CA Backbone Structure
        print(f"Creating CA Backbone for {pdb_file}")
        xyz = create_backbone(pdb_file)
        xyz = xyz[['X', 'Y', 'Z']]
    else:  # Structure Simplification
        xyz = create_structure(structure_num, pdb_file, pdb_id, multiprocess_toggle)

    print(f"Created {structure_name[structure_num]} Structure for {pdb_id}")
    print(f"Printing XYZ for {structure_name[structure_num]} Structure...")
    print('-' * 50)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(xyz)
    print('-' * 50)

    if report_toggle:
        create_report(pdb_id, xyz, structure_name[structure_num])
    if output_xyz_file is not None:
        xyz.to_csv(output_xyz_file, index=False)
    if output_pdb_file is not None:
        create_modified_pdb(pdb_id, xyz, structure_name[structure_num])
    if no_footprint_toggle:
        if os.path.exists(pdb_file):
            os.remove(pdb_file)
        if os.path.exists(f"GenerateOutput/PDB_Files/{pdb_id}_modified.pdb"):
            os.remove(f"GenerateOutput/PDB_Files/{pdb_id}_modified.pdb")
    if visualize_toggle:
        plot_structure(xyz, title=f"{structure_name[structure_num]} Structure ({str(structure_num)}) for {pdb_id}")


def argument_parser():
    # Create the parser
    parser = argparse.ArgumentParser(description='Convert a PDB file or PDB code to a Simplified Structure.')

    # Add the arguments
    parser.add_argument('pdb', metavar='pdb', type=str, nargs='?',
                        help='input a PDB code or a PDB filepath')
    parser.add_argument('structure', metavar='structure', type=int, nargs='?',
                        help='input the number of moves for the structure you want to create (1, 4, 6, 8, 12)')
    parser.add_argument('-v', '--visualize', action='store_true',
                        help='visualize the structure using matplotlib')
    parser.add_argument('-r', '--report', action='store_true',
                        help='generate a report in the GenerateOutput/Reports folder')
    parser.add_argument('-o-xyz', '--output_xyz', metavar='FILENAME', type=str,
                        help='output new structure xyz into given filename')
    parser.add_argument('-o-pdb', '--output_pdb', metavar='FILENAME', type=str,
                        help='output new structure PDB into given filename')
    parser.add_argument('-m', '--multiprocess_off', action='store_true',
                        help='turn off multiprocess for fitting algorithm')
    parser.add_argument('-nf', '--no_footprint', action='store_true',
                        help='deleting pdb files after use')

    # Execute the parse_args() method
    user_inputs = parser.parse_args()
    return user_inputs


if __name__ == '__main__':
    # Get Arguments
    args = argument_parser()

    pdb_code = args.pdb
    structure = args.structure
    visualize = args.visualize
    report = args.report
    output_xyz = args.output_xyz
    output_pdb = args.output_pdb
    multiprocess = args.multiprocess_off
    no_footprint = args.no_footprint

    changed_pdb = False
    if pdb_code is None:
        changed_pdb = True
        replace = False
        while not replace:
            pdb_code = ''
            while len(pdb_code) != 4:
                print("Input the 4-Letter PDB Code for the Protein you want to create a Structure for:")
                print("Sample PDB Codes are 1A0M, 1A1M, 1A2M, 1A3M, 1A4M, "
                      "1A5M, 1A6M, 1A7M, 1A8M, 1A9M, 1B0M, 1B1M, 1B2M, 1B3M, 1B4M...")
                pdb_code = input("Input 4-Letter PDB Code: ")

            if check_pdb_is_valid(pdb_code):
                replace = True

    # Get the PDB file
    pdb_filepath = ""
    if len(pdb_code) == 4:
        pdb_filepath = download_pdb(pdb_code)
    else:
        pdb_filepath = pdb_code
        pdb_code = pdb_filepath.split('/')[-1].split('.')[0]

    if changed_pdb:
        num_chains = count_chains_in_pdb(pdb_code)
        if num_chains > 1:
            print(f"WARNING: {pdb_code} contains {num_chains} chains. "
                  f"The program will treat the protein as a single continuous chain.")
            override = "-1"
            while override not in ["Y", "N"]:
                override = input("Do you want to override the warning? (Y/N): ")
            if override == "N":
                exit(0)
    else:
        num_chains = count_chains_in_pdb(pdb_code)
        if num_chains > 1:
            print(f"WARNING: {pdb_code} contains {num_chains} chains. "
                  f"The program will treat the protein as a single continuous chain.")

    if structure is None:
        while structure not in ["1", "4", "6", "8", "12"]:
            print("Input the Number for the Structure you want to create:")
            print("1  = CA BACKBONE")
            print("4  = SQUARE TILING")
            print("6  = CUBIC HONEYCOMB")
            print("8  = TRIANGULAR PRISMATIC HONEYCOMB")
            print("12 = TETRAHEDRAL-OCTAHEDRAL HONEYCOMB")
            structure = input("Input Structure: ")
        structure = int(structure)

    # Execute the main function
    execute(pdb_code, pdb_filepath, structure, visualize,
            report, output_xyz, output_pdb, multiprocess, no_footprint)
