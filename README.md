# PDB2Lattice: README
### Alexander J. Habegger

## Overview

PDB2LatticePy stands at the forefront of simplifying protein structures. Its primary mission is to untangle the complexities inherent in protein data, transforming PDB files or IDs into more digestible and manageable forms. The software specializes in converting detailed protein structures of the Protein Data Bank into simplified models such as the CA Backbone, Square Tiling, and various honeycomb structures. These models are not only more comprehensible but also retain the crucial structural information necessary for computation.

### Computational Efficiency

By simplifying structures, it remarkably reduces the computational power required for processing. This aspect is crucial when dealing with large datasets or when integrating protein models into extensive machine learning frameworks. Researchers and developers working on advanced computational projects, such as those involving large-scale simulations or newer quantum annealing strategies, will find this efficiency particularly beneficial. It allows for faster computations and analyses, making it a practical tool for both high-powered research and educational purposes.

### User-Centric Design

The tool is crafted with a focus on user experience. It accommodates various inputs and command-line arguments, enabling customization to meet diverse research needs and personal preferences. This user-centric design philosophy ensures that PDB2LatticePy is accessible to a wide range of users, from seasoned researchers to students just beginning their exploration of protein structures.

## Related Repositories

- [Lattice-2-Backbone](https://github.com/ahabegger/Lattice-2-Backbone): This repository contains the inverse of PDB2Lattice, converting simplified structures into CA Backbones.

- [Quantum-Protein-Lattice-Folding](https://github.com/ahabegger/Quantum-Protein-Lattice-Folding): This repository contains the code for the Quantum Protein Lattice Folding project, which uses PDB2Lattice to generate simplified structures for quantum computing simulations.

## Types of Simplified Structures

PDB2Lattice offers the capability to transform complex protein structures into various simplified models, each providing unique insights and perspectives. The tool supports the following types of simplified structures:

1. **CA Backbone**: This model represents the most fundamental aspect of a protein's structure, focusing solely on the alpha carbon (CA) atoms in the protein's backbone.

2. **Square Tiling**: This 2D model is derived from the CA Backbone, projecting the protein structure onto a two-dimensional plane. It simplifies the structure into a grid-like pattern, making it easier to observe and analyze the protein's topology in a planar format.

3. **Cubic Honeycomb**: Elevating the representation to three dimensions, the Cubic Honeycomb model extends the CA Backbone into a 3D lattice. This model offers a more spatially comprehensive view, portraying how the protein's structure occupies three-dimensional space. 

4. **Triangular Prismatic Honeycomb**: This model further sophisticates the 3D representation by incorporating triangular prismatic elements into the honeycomb structure. It offers an intricate view of the protein's structure, highlighting the complex interplay between its components in three dimensions. This model is particularly useful for detailed structural analysis and spatial understanding of the protein.

5. **Tetrahedral-Octahedral Honeycomb**: The most complex model in the suite, this structure uses a combination of tetrahedral and octahedral elements to represent the protein's backbone in 3D. This model provides an exceptionally detailed and nuanced view of the protein structure, allowing for an in-depth analysis of its spatial configuration and interactions. It is ideal for advanced studies where detailed spatial relationships within the protein are critical.

## Usage

### Installation

To use PDB2LatticePy, first ensure you have Python installed on your system. Clone or download the repository. 

```bash
git clone https://github.com/ahabegger/PDB-2-Lattice.git
```
or 
```bash
git clone git@github.com:ahabegger/PDB-2-Lattice.git
```

Then navigate to the directory containing `main.py`. This script is the entry point for processing PDB files or IDs.

### Command-Line Arguments

The `main.py` script is designed to be run from the command line with several arguments that control its behavior. If no arguments are provided, the script will prompt you to enter the necessary information.

Required Arguments:

1. `pdb`: Specify the PDB code or the filepath to a PDB file. Example PDB codes are `1A0M`, `1A1M`, etc. If this argument is not provided, the script will prompt you to enter a valid 4-letter PDB code.

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
python main.py 1A0M 4 -v -r --output_xyz "output_structure.xyz" --output_pdb "output_structure.pdb"
```

This command processes the PDB code `1A0M`, creates a Square Tiling structure, visualizes it, generates a report, and outputs the results in XYZ and PDB formats.

### Handling Multiple Chains

If the provided PDB code contains multiple chains, the script will warn you. You can choose to override this warning and treat the protein as a single continuous chain.

### Output

Upon successful execution, the script will:
- Print the XYZ coordinates of the created structure.
- Generate visualization plots (if `-v` is used).
- Create a detailed report (if `-r` is used).
- Output the structure in both XYZ and PDB formats (if specified).

## Features

- **main.py**: This is the core script of the repository. It processes protein structures from PDB files or IDs, converting them into simplified structural representations. The script offers functionalities for creating various structural models (e.g., CA Backbone, Cubic Honeycomb), generating reports, visualizing structures, and exporting results in XYZ or PDB formats. It is designed to handle user input and command-line arguments to customize the processing according to specific requirements.

- **Structures.py**: This script is responsible for generating a structure based on input parameters such as the number of moves and a PDB file. It optimizes the structure using tilt and fitting algorithms, starting with constructing a backbone structure from a PDB file, defining movements, and then applying optimization techniques to refine the structure, finally returning the optimized XYZ coordinates.

- **Tilting.py**: This module defines functions for optimizing the tilt of a set of movements with respect to a backbone structure defined by XYZ coordinates. The primary function, `optimize_tilt`, iteratively rotates the movements in 3D space, evaluating each rotation using a cost function to find the optimal combination of movements. Auxiliary functions like `rotate_movements`, `create_cost_matrix`, and `get_cost` support this process.

- **PDB2Backbone.py**: This script is used to parse a given PDB file and extract the backbone structure of a protein. It creates a DataFrame containing the amino acid sequence and the corresponding X, Y, Z coordinates of each alpha carbon (CA) atom in the protein's backbone, facilitating further analysis or manipulation.

- **Fitting.py**: This script focuses on optimizing a set of movements based on a cost matrix. It can use multiprocessing for parallel execution and includes functions for iteratively refining movements to achieve the lowest possible cost, using techniques like local search refinement and testing different combinations of movements.

- **GenerateReport.py**: This script is designed to generate comprehensive reports for protein structures transformed using PDB2Lattice. It involves downloading PDB files, creating modified PDB files, generating diagrams for visualization, and compiling all this information into detailed HTML reports. These reports include comparisons between the original and modified structures, along with interactive diagrams and structural data.

## Contributions

Contributions to PDB2LatticePy are welcome. Whether it's improving the code, adding new features, or fixing bugs, feel free to fork the repository and submit your pull requests.

### Potential Contributions

- **Multi-Chain Support**: The current version of PDB2LatticePy does not support multiple chains. 

- **Options for Allowing Different Test Batteries for Fitting Algorithm**: The fitting algorithm currently uses a fixed set of test batteries. It would be useful to allow users to specify different test batteries for the algorithm.

- **Options for Allowing Different Cost Functions for Fitting Algorithm**: The fitting algorithm currently uses a fixed cost function. It would be useful to allow users to specify different cost functions for the algorithm. For Example, the similarity of current XYZ points in structure to that of the backbone structure.

- **Improvements to the Tilt Algorithm**: The tilt algorithm currently uses a fixed set of movements. It would be useful to allow users to specify different movements for the algorithm.

- **Generating Reports for Multiple Structures**: The current version of PDB2LatticePy only supports generating reports for a single structure. It would be useful to allow users to generate reports for multiple structures.

- **Improvements to the Report Generation**: The current version of PDB2LatticePy generates reports information in an unclear format. It would be useful to improve the report generation to make it more readable and user-friendly.

## License

PDB2LatticePy is open-source software licensed under MIT License. Users are free to modify and distribute the software under the terms of this license.
