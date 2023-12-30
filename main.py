from GenerateReport import create_report
from PDB2Backbone import create_backbone
from OneDimCubic/OneDimCubic import create_one_dim_cubic
from ThreeDimCubic/ThreeDimCubic import create_three_dim_cubic
from TetrahederalLattice/TetrahederalLattice import create_tetrahederal_lattice
from NDimensionalLattice/NDimensionalLattice import create_n_dimensional_lattice


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
    create_backbone(pdb_code)
elif structure == "2":
    create_one_dim_cubic(pdb_code)
elif structure == "3":
    create_three_dim_cubic(pdb_code)
elif structure == "4":
    create_tetrahederal_lattice(pdb_code)
elif structure == "5":
    create_n_dimensional_lattice(pdb_code)
else:
    print("Invalid Structure")
    exit()
