from GenerateReport import create_report
from PDB2Backbone import create_backbone
from OneDimCubic.OneDimCubic import create_one_dim_cubic
from ThreeDimCubic.ThreeDimCubic import create_three_dim_cubic
from Tetrahederal.Tetrahederal import create_tetrahedral_lattice
from NDimLattice.NDimLattice import create_n_dimensional_lattice

is_test = True
structure = "1"
pdb_code = "1A2M"

if not is_test:
    print("Sample PDB Codes are 1A0M, 1A1M, 1A2M, 1A3M, 1A4M, 1A5M, 1A6M, 1A7M, 1A8M, 1A9M, 1B0M, 1B1M, 1B2M, 1B3M, 1B4M")
    pdb_code = input("Input 4-Letter PDB Code: ")

    print("Structure Options:")
    print("1 = CA Backbone Structure")
    print("2 = 1-Dimensional Cubic Lattice Structure")
    print("3 = 3-Dimensional Cubic Lattice Structure")
    print("4 = Tetrahedral Lattice Structure")
    print("5 = N-Dimensional Lattice Structure")
    structure = input("Input Structure: ")

if structure == "1":
    xyz = create_backbone(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "CA Backbone Structure")
elif structure == "2":
    xyz = create_one_dim_cubic(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "1-Dimensional Cubic Lattice Structure")
elif structure == "3":
    xyz = create_three_dim_cubic(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "3-Dimensional Cubic Lattice Structure")
elif structure == "4":
    xyz = create_tetrahedral_lattice(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "Tetrahedral Lattice Structure")
elif structure == "5":
    xyz = create_n_dimensional_lattice(pdb_code)
    print(xyz)
    create_report(pdb_code, xyz, "N-Dimensional Lattice Structure")
else:
    print("Invalid Structure")
    exit()

