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
This Script takes a PDB code and a structure type and creates a report containing the original PDB file, the modified
PDB file, and the diagrams of both.
'''


def user_input():
    print("Sample PDB Codes are 1A0M, 1A1M, 1A2M, 1A3M, 1A4M, "
          "1A5M, 1A6M, 1A7M, 1A8M, 1A9M, 1B0M, 1B1M, 1B2M, 1B3M, 1B4M")
    user_pdb = input("Input 4-Letter PDB Code: ")

    print("Input the Number for the Structure you want to create:")
    print("1  = CA BACKBONE")
    print("4  = SQUARE TILING")
    print("6  = CUBIC HONEYCOMB")
    print("8  = TRIANGULAR PRISMATIC HONEYCOMB")
    print("12 = TETRAHEDRAL-OCTAHEDRAL HONEYCOMB")

    structure = input("Input Structure: ")

    return user_pdb, structure


def menu(pdb_code, structure, visualize=True):
    if structure == "1":  # CA Backbone Structure
        xyz, cost, time = create_backbone(pdb_code), 0, 0
        if visualize:
            plot_structure(xyz[['X', 'Y', 'Z']], title="CA Backbone Structure")
        create_report(pdb_code, xyz, "CA Backbone Structure")
    else:
        xyz, cost, time = create_lattice(int(structure), pdb_code)
        if visualize:
            plot_structure(xyz, title=f"{structure} Move Lattice for {pdb_code}")
        create_report(pdb_code, xyz, f"{structure} Move")

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
    pdb2 = "1TNM"
    menu(pdb2, "4", visualize=True)
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

