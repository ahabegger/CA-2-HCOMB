from GenerateReport import create_report, view_pdb
from Structure import Structure


pdb_code, nonstandard, structure = 0, 0, 0

model = ""
with open(f"PDB_Files/{pdb_code}.pdb") as file:
    for line in file:
        model += line

s1 = Structure(model, nonstandard)

new_lines = f'HEADER Modification of {pdb_code} PDB Code\n' \
            f'REMARK Included Atoms : \'CA\'\n' \
            f'REMARK Include Nonstandard Amino Acids: {nonstandard}\n' \
            f'REMARK Structure: {structure}\n' \

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
