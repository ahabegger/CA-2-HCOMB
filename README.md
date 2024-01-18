![PDB2Lattice](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/fb1433d3-45bc-4e03-8d53-4cbb5c65444a)

# PDB2Lattice: README

PDB2Lattice stands at the forefront of simplifying protein structures. Its primary mission is to untangle the complexities inherent in protein data, transforming PDB files or IDs into more digestible and manageable forms. The software specializes in converting detailed protein structures of the Protein Data Bank into simplified models such as the CA Backbone, Square Tiling, and various honeycomb structures. These models are more comprehensible and retain the crucial structural information necessary for computation.

### Computational Efficiency

Simplifying structures remarkably reduces the computational power required for processing. This aspect is crucial when dealing with large datasets or integrating protein models into extensive machine-learning frameworks. Researchers and developers working on advanced computational projects, such as those involving large-scale simulations or newer quantum annealing strategies, will find this efficiency particularly beneficial. It allows for faster computations and analyses, making it a practical tool for both high-powered research and educational purposes.

### User-Centric Design

The tool is crafted with a focus on user experience. It accommodates various inputs and command-line arguments, enabling customization to meet diverse research needs and personal preferences. This user-centric design philosophy ensures that PDB2Lattice is accessible to a wide range of users, from seasoned researchers to students just beginning their exploration of protein structures.

## Related Repositories

- [Lattice-2-Backbone](https://github.com/ahabegger/Lattice-2-Backbone): This repository contains the inverse of PDB2Lattice, converting simplified structures into CA Backbones.

- [Quantum-Protein-Lattice-Folding](https://github.com/ahabegger/Quantum-Protein-Lattice-Folding): This repository contains the code for the Quantum Protein Lattice Folding project, which uses PDB2Lattice to generate simplified structures for quantum computing simulations.

## Types of Simplified Structures

PDB2Lattice can transform complex protein structures into simplified models, each providing unique insights and perspectives. All simplification structures have an edge that is one unit long and is composed of convex shapes. These requirements allow the exclusion principle to be followed by making the alpha carbons placed at the vertices not too close to one another. The edges within the models represent the connection between consecutive amino acids. The tool supports the following types of simplified structures:

1. **Square Tiling**: A 2D geometric pattern where squares of identical size are arranged side by side, covering a plane without gaps or overlaps. The 2D model is derived from the XYZ coordinates of the alpha carbon backbone in the PDB file by having the amino acids projected onto the 2D plane. The simplification limits movement from one amino acid to another into 4 valid movements represented by [x, y]: [1, 0], [-1, 0], [0, 1], and [0, -1]. 

![square_tiling](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/be712d5b-aebd-4b24-ac7a-dcf0e99d76fc)

2. **Cubic Honeycomb**: A 3D geometric structure of cubes arranged in a continuous pattern. This honeycomb tessellation features cubes that are aligned and stacked in such a way as to fill space without any gaps or overlaps, showcasing perfect symmetry and uniformity. Elevating the representation to three dimensions, the Cubic Honeycomb model extends the alpha carbon backbone into a 3D lattice. This model offers a more spatially comprehensive view, portraying how the protein's structure occupies three-dimensional space. The simplification limits movement from one amino acid to another into 6 valid movements represented [x, y, z]: [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1] and [0, 0, -1].

![cubic_honeycomb](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/55161819-cbc0-407b-9a09-c8fe663e0dfe)

3. **Triangular Prismatic Honeycomb**: A spatial tessellation formed by stacking triangular prisms in a continuous, repeating pattern. This honeycomb structure is characterized by its uniform, three-sided prisms arranged to fill the space without gaps or overlaps. The simplification limits movement from one amino acid to another into 8 valid movements represented [x, y, z]: [sqrt_3_div_2, 0.5, 0], [-sqrt_3_div_2, 0.5, 0], [0, 1, 0], [sqrt_3_div_2, -0.5, 0], [-sqrt_3_div_2, -0.5, 0], [0, -1, 0], [0, 0, 1], and [0, 0, -1].

![triangular_prismatic_honeycomb](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/0a20ea09-f43b-4c73-a93f-7a6e81c33938)

4. **Tetrahedral-Octahedral Honeycomb**: A complex 3D geometric structure where tetrahedra and octahedra interlock in a repeating pattern. The most complex model in the suite, this structure uses a combination of tetrahedral and octahedral elements to represent the protein's backbone in 3D. The simplification limits movement from one amino acid to another into 12 valid movements represented [x, y, z]: [sqrt_2_div_2, sqrt_2_div_2, 0], [sqrt_2_div_2, 0, sqrt_2_div_2], [0, sqrt_2_div_2, sqrt_2_div_2], [-sqrt_2_div_2, -sqrt_2_div_2, 0], [-sqrt_2_div_2, 0, -sqrt_2_div_2], [0, -sqrt_2_div_2, -sqrt_2_div_2], [sqrt_2_div_2, -sqrt_2_div_2, 0], [sqrt_2_div_2, 0, -sqrt_2_div_2], [0, sqrt_2_div_2, -sqrt_2_div_2], [-sqrt_2_div_2, sqrt_2_div_2, 0], [-sqrt_2_div_2, 0, sqrt_2_div_2], [0, -sqrt_2_div_2, sqrt_2_div_2].

![tetrahedral_octahedral_honeycomb](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/4f8b55d5-1067-4fc9-9fd6-49d04a338fe2)

## Usage

### Installation

To use PDB2Lattice, please make sure you have Python installed on your system. Clone or download the repository using one of the following commands: 

```bash
git clone https://github.com/ahabegger/PDB-2-Lattice.git
git clone git@github.com:ahabegger/PDB-2-Lattice.git
```

Then, navigate to the directory containing `main.py`. This script is the entry point for processing PDB files or IDs, but before that the required dependencies (pandas~=2.1.3, numpy~=1.26.2, requests~=2.31.0, nglview~=3.0.8, matplotlib~=3.8.2, bio~=1.6.0 ) must be downloaded by running the following command:

```bash
pip install -r requirements.txt
```

### Command-Line Arguments

The `main.py` script is designed to be run from the command line with several arguments that control its behavior. The script will prompt you to enter the necessary information if you don't get any arguments.

Required Arguments:

1. `pdb`: Specify the PDB code or the file path to a PDB file. For example, PDB codes are `1A0M`, `1A1M`, etc. The script will prompt you to enter a valid 4-letter PDB code if this argument is not provided.

2. `structure`: Enter the number corresponding to the structure type you wish to create. The options are:
   - `1` for CA Backbone
   - `4` for Square Tiling
   - `6` for Cubic Honeycomb
   - `8` for Triangular Prismatic Honeycomb
   - `12` for Tetrahedral-Octahedral Honeycomb

Optional Arguments:

3. `-v` or `--visualize`: Use this flag to visualize the structure using Matplotlib.

4. `-r` or `--report`: This flag triggers the generation of a report in the `GenerateOutput/Reports` folder.

5. `-o-xyz` or `--output_xyz`: Specify a filename to output the new structure XYZ data.

6. `-o-pdb` or `--output_pdb`: Specify a filename to output the new structure PDB file.

7. `-m` or `--multiprocess_off`: Use this flag to turn off multiprocess for the fitting algorithm.

8. `-nf` or `--no_footprint`: Use this flag to delete PDB files after use.

### Running the Script

Run `main.py` from the command line, providing the necessary arguments. For example:

```bash
python main.py 1A0M 6 -v -r --output_xyz "output_structure.xyz" --output_pdb "output_structure.pdb"
```

This command processes the PDB code `1A0M`, creates a Square Tiling structure, visualizes it, generates a report, and outputs the results in XYZ and PDB formats. Here is the visualization of the Square Tiling structure for the PDB code `1A0M`:

![1A0M](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/aea10afb-1893-4a1f-b26b-e747f70705fa)

### Handling Multiple Chains

The script will warn you if the provided PDB code contains multiple chains. You can override this warning and treat the protein as a single continuous chain.

### Output

Upon successful execution, the script will:
- Print the XYZ coordinates of the created structure.
- Generate visualization plots (if `-v` is used).
- Create a detailed report (if `-r` is used).
- Output the structure in XYZ and PDB formats (if specified).

## Features

- **main.py**: This is the core script of the repository. It processes protein structures from PDB files or IDs, converting them into simplified structural representations. The script offers functionalities for creating various structural models (e.g., CA Backbone, Cubic Honeycomb), generating reports, visualizing structures, and exporting results in XYZ or PDB formats. It is designed to handle user input and command-line arguments to customize the processing according to specific requirements.

- **Structures.py**: This script generates a structure based on input parameters such as the number of moves and a PDB file. It optimizes the structure using tilt and fitting algorithms, starting with constructing a backbone structure from a PDB file, defining movements, applying optimization techniques to refine the structure, and finally returning the optimized XYZ coordinates.

- **Tilting.py**: This module defines functions for optimizing the tilt of a set of movements concerning a backbone structure defined by XYZ coordinates. The primary function, `optimize_tilt`, iteratively rotates the movements in 3D space, evaluating each rotation using a cost function to find the optimal combination of movements. Auxiliary functions like `rotate_movements`, `create_cost_matrix`, and `get_cost` support this process.

- **PDB2Backbone.py**: This script is used to parse a given PDB file and extract the backbone structure of a protein. It creates a DataFrame containing the amino acid sequence and the corresponding X, Y, Z coordinates of each alpha carbon (CA) atom in the protein's backbone, facilitating further analysis or manipulation.

- **Fitting.py**: This script optimizes movements based on a cost matrix. It can use multiprocessing for parallel execution and includes functions for iteratively refining movements to achieve the lowest possible cost, using techniques like local search refinement and testing different combinations of movements.

- **GenerateReport.py**: This script is designed to generate comprehensive reports for protein structures transformed using PDB2Lattice. It involves downloading PDB files, creating modified PDB files, generating diagrams for visualization, and compiling all this information into detailed HTML reports. These reports include original and modified structures, interactive diagrams, and structural data comparisons.

## Contributions

Contributions to PDB2Lattice are welcome. Whether it's improving the code, adding new features, or fixing bugs, feel free to fork the repository and submit your pull requests.

### Potential Contributions

- **Multi-Chain Support**: The current version of PDB2Lattice does not support multiple chains. 

- **Options for Allowing Different Test Batteries for Fitting Algorithm**: The fitting algorithm currently uses a fixed set of test batteries. Allowing users to specify different test batteries for the algorithm would be helpful.

- **Options for Allowing Different Cost Functions for Fitting Algorithm**: The fitting algorithm currently uses a fixed cost function. It would be helpful to allow users to specify different cost functions for the algorithm. For Example, the similarity of current XYZ points in structure to that of the backbone structure.

- **Improvements to the Tilt Algorithm**: The tilt algorithm currently uses a fixed set of movements. Allowing users to specify different movements for the algorithm would be helpful.

- **Generating Reports for Multiple Structures**: The current version of PDB2Lattice only supports generating reports for a single structure. It would be helpful to allow users to generate reports for multiple structures.

- **Improvements to the Report Generation**: The current version of PDB2Lattice generates report information in an unclear format. It would be helpful to improve the report generation to make it more readable and user-friendly.

## License

PDB2Lattice is open-source software licensed under MIT License. Users are free to modify and distribute the software under the terms of this license.
