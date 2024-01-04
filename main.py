from GenerateReport import create_report
from PDB2Backbone import create_backbone
from Tetrahederal.Tetrahederal import create_tetrahedral
from Hexahedral.Hexahedral import create_hexahedral
from Octahedral.Octahedral import create_octahedral
from Dodecahedral.Dodecahedral import create_dodecahedral
from Icosahedral.Icosahedral import create_icosahedral

'''
main.py
This Script takes a PDB code and a structure type and creates a report containing the original PDB file, the modified
PDB file, and the diagrams of both.
'''

is_test = True
structure = "4"
pdb_code = "1A2M"

if not is_test:
    print("Sample PDB Codes are 1A0M, 1A1M, 1A2M, 1A3M, 1A4M, "
          "1A5M, 1A6M, 1A7M, 1A8M, 1A9M, 1B0M, 1B1M, 1B2M, 1B3M, 1B4M")
    pdb_code = input("Input 4-Letter PDB Code: ")

    print("Platonic Solids Structure Options:")
    print("1 = CA Backbone Structure")
    print("2 = Tetrahedral (4 Moves) Lattice Structure")
    print("3 = Hexahedral (6 Moves) Lattice Structure")
    print("4 = Octahedral (8 Moves) Lattice Structure")
    print("5 = Dodecahedron (12 Moves) Lattice Structure")
    print("6 = Icosahedron (20 Moves) Lattice Structure")
    structure = input("Input Structure: ")

if structure == "1":  # CA Backbone Structure
    xyz = create_backbone(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "CA Backbone Structure")
elif structure == "2":  # Tetrahedral (4 Moves) Lattice Structure
    xyz = create_tetrahedral(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "Hexahedral Lattice Structure")
elif structure == "3":  # Hexahedral (6 Moves) Lattice Structure
    xyz = create_hexahedral(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "Hexahedral Lattice Structure")
elif structure == "4":  # Octahedral (8 Moves) Lattice Structure
    xyz = create_octahedral(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "Octahedral Lattice Structure")
elif structure == "5":  # Dodecahedron (12 Moves) Lattice Structure
    xyz = create_dodecahedral(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "Dodecahedral Lattice Structure")
elif structure == "6":  # Icosahedron (20 Moves) Lattice Structure
    xyz = create_icosahedral(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "Icosahedral Lattice Structure")
else:
    print("Invalid Structure")
    exit()

