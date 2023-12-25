from Structures import OneDimCubic as onecube
from Structures import ThreeDimCubic as threecube
from Structures import Tetrahederal as tetra

class Structure:
    def __init__(self, model, nonstandard):
        included_lines = ["ATOM"]

        self.atom_lines = ''
        self.seq_lines = ''
        start = 1

        if nonstandard:
            included_lines.append("HETATM")

        for line in model.splitlines():
            if line.split()[0] in included_lines:
                if line.split()[2] in ['CA']:
                    self.atom_lines += f"{line[:7]}{start:>4}{line[11:]}" + '\n'
                    start += 1
            elif line.split()[0] in ["SEQRES"]:
                self.seq_lines += line + '\n'

        self.input_xyz = self.parse_xyz()
        self.output_xyz = self.input_xyz

    def parse_xyz(self):
        xyz_array = []

        for line in self.atom_lines.splitlines():
            coordinates = line.split()
            xyz_array.append([float(coordinates[6]), float(coordinates[7]), float(coordinates[8])])

        return xyz_array

    def default(self):
        return self.seq_lines, self.atom_lines

    def one_d_cubic(self):
        self.output_xyz = onecube.convert_xyz(self.input_xyz)
        print(self.output_xyz)
        self.atom_lines = self.replace_xyz()
        return self.seq_lines, self.atom_lines

    def three_d_cubic(self):
        self.output_xyz = threecube.convert_xyz(self.input_xyz)
        self.atom_lines = self.replace_xyz()
        return self.seq_lines, self.atom_lines

    def tetrahederal(self):
        self.output_xyz = tetra.convert_xyz(self.input_xyz)
        self.atom_lines = self.replace_xyz()
        return self.seq_lines, self.atom_lines

    def replace_xyz(self):
        new_atom_lines = ''
        split_lines = self.atom_lines.splitlines()
        for x in range(len(split_lines)):
            print(split_lines[x])
            replace_line = self.replace_coordinates(split_lines[x], self.output_xyz[x])
            print(replace_line)
            new_atom_lines += replace_line + '\n'

        return new_atom_lines

    def replace_coordinates(self, atom_line, new_coords):
        # Ensure the new coordinates are in the correct format (right-aligned within 8 characters)
        formatted_coords = [f"{coord:8.3f}" for coord in new_coords]

        # Replace the coordinates in the line
        new_line = (
                atom_line[:30] +  # Everything before the X coordinate
                formatted_coords[0] +  # New X coordinate
                formatted_coords[1] +  # New Y coordinate
                formatted_coords[2] +  # New Z coordinate
                atom_line[54:]  # Everything after the Z coordinate
        )

        return new_line
    def print(self):
        print(self.seq_lines)
        print(self.atom_lines)
        print(self.input_xyz)
        print(self.output_xyz)


if __name__ == "__main__":
    model = ""
    with open(f"PDB_Files/2WFU.pdb") as file:
        for line in file:
            model += line

    s1 = Structure(model, True)
    print(s1.one_d_cubic())
