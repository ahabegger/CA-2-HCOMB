from GenerateReport import create_report, view_pdb
from Structure import Structure

print("Sample PDB Codes are 1A0M, 1A1M, 1A2M, 1A3M, 1A4M, 1A5M, 1A6M, 1A7M, 1A8M, 1A9M, 1B0M, 1B1M, 1B2M, 1B3M, 1B4M")
pdb_code = input("Input 4-Letter PDB Code: ")

print("Structure Options:")
print("1 = CA Backbone Structure")
print("2 = 1-Dimensional Cubic Lattice Structure")
print("3 = 3-Dimensional Cubic Lattice Structure")
print("4 = Tetrahedral Lattice Structure")
print("5 = N-Dimensional Lattice Structure")
structure = input("Input Structure: ")


model = ""
with open(f"PDB_Files/{pdb_code}.pdb") as file:
    for line in file:
        model += line

s1 = Structure(model)

new_lines = f'HEADER Modification of {pdb_code} PDB Code\n' \
            f'REMARK Structure: {structure}\n'

seq_lines = ''
atom_lines = ''

if structure == "DEFAULT STRUCTURE":
    seq_lines, atom_lines = s1.default()
elif structure == "1-DIMENSIONAL CUBIC LATTICE STRUCTURE":
    seq_lines, atom_lines = s1.one_d_cubic()
elif structure == "3-DIMENSIONAL CUBIC LATTICE STRUCTURE":
    seq_lines, atom_lines = s1.three_d_cubic()
elif structure == "TETRAHEDERAL LATTICE STRUCTURE":
    seq_lines, atom_lines = s1.tetrahederal()

new_lines += seq_lines
new_lines += atom_lines
new_lines += 'END'

with open(f'Modified_PDB_Files/{pdb_code}_modified.pdb', 'w') as file:
    file.write(new_lines)

view_pdb(f"Modified_PDB_Files/{pdb_code}_modified.pdb")
view_pdb(f"PDB_Files/{pdb_code}.pdb")

create_report(pdb_code)

