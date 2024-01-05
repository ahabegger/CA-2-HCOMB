from GenerateReport import create_report
from PDB2Backbone import create_backbone
from Structures.Tetrahederal import create_tetrahedral
from Structures.Hexahedral import create_hexahedral
from Structures.Octahedral import create_octahedral
from Structures.Icosahedral import create_icosahedral
from Structures.Dodecahedral import create_dodecahedral
import Visualization as plot

'''
main.py
This Script takes a PDB code and a structure type and creates a report containing the original PDB file, the modified
PDB file, and the diagrams of both.
'''


def user_input():
    print("Sample PDB Codes are 1A0M, 1A1M, 1A2M, 1A3M, 1A4M, "
          "1A5M, 1A6M, 1A7M, 1A8M, 1A9M, 1B0M, 1B1M, 1B2M, 1B3M, 1B4M")
    pdb_code = input("Input 4-Letter PDB Code: ")

    print("Platonic Solids Structure Options:")
    print("1 = CA Backbone Structure")
    print("2 = Tetrahedral (4 Moves) Lattice Structure")
    print("3 = Hexahedral (6 Moves) Lattice Structure")
    print("4 = Octahedral (8 Moves) Lattice Structure")
    print("5 = Icosahedral (12 Moves) Lattice Structure")
    print("6 = Dodecahedral (20 Moves) Lattice Structure")
    structure = input("Input Structure: ")

    return pdb_code, structure


def menu(pdb_code, structure):

    if structure == "1":  # CA Backbone Structure
        xyz, cost = create_backbone(pdb_code), 0
        plot.visualize(xyz[['X', 'Y', 'Z']], title="CA Backbone Structure")
        #  create_report(pdb_code, xyz, "CA Backbone Structure")

    elif structure == "2":  # Tetrahedral (4 Moves) Lattice Structure
        xyz, cost = create_tetrahedral(pdb_code)
        plot.visualize(xyz, title="Tetrahedral (4 Move) Lattice")
        #  create_report(pdb_code, xyz, "Tetrahedral Lattice Structure")

    elif structure == "3":  # Hexahedral (6 Moves) Lattice Structure
        xyz, cost = create_hexahedral(pdb_code)
        plot.visualize(xyz, title="Hexahedral (6 Move) Lattice")
        #  create_report(pdb_code, xyz, "Hexahedral Lattice Structure")

    elif structure == "4":  # Octahedral (8 Moves) Lattice Structure
        xyz, cost = create_octahedral(pdb_code)
        plot.visualize(xyz, title="Octahedral (8 Move) Lattice")
        #  create_report(pdb_code, xyz, "Octahedral Lattice Structure")

    elif structure == "5":  # Icosahedral (12 Moves) Lattice Structure
        xyz, cost = create_icosahedral(pdb_code)
        plot.visualize(xyz, title="Icosahedral (12 Move) Lattice")
        #  create_report(pdb_code, xyz, "Icosahedral Lattice Structure")

    elif structure == "6":  # Dodecahedral (20 Moves) Lattice Structure
        xyz, cost = create_dodecahedral(pdb_code)
        plot.visualize(xyz, title="Icosahedral (12 Move) Lattice")
        #  create_report(pdb_code, xyz, "Dodecahedral Lattice Structure")

    else:
        print("Invalid Structure")
        exit()


if __name__ == '__main__':
    # pdb_code, structure = user_input()

    structure = "4"
    pdb_code = "1A2M"

    menu(pdb_code, structure)
