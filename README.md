![CA-2-HCOMB](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/fb1433d3-45bc-4e03-8d53-4cbb5c65444a)

# CA-2-HCOMB: README

CA-2-HCOMB is a repository by Alexander J. Habegger and stands at the forefront of simplifying protein structures. Its primary mission is to untangle the complexities inherent in protein data, transforming PDB files or IDs into more digestible and manageable forms. The software specializes in converting detailed protein structures of the Protein Data Bank into simplified models such as the CA Backbone, Square Tiling, and various honeycomb structures. These models are more comprehensible and retain the crucial structural information necessary for computation.

### Computational Efficiency

Simplifying structures remarkably reduces the computational power required for processing. This aspect is crucial when dealing with large datasets or integrating protein models into extensive machine-learning frameworks. Researchers and developers working on advanced computational projects, such as those involving large-scale simulations or newer quantum annealing strategies, will find this efficiency particularly beneficial. It allows for faster computations and analyses, making it a practical tool for both high-powered research and educational purposes.

### User-Centric Design

The tool is crafted with a focus on user experience. It accommodates various inputs and command-line arguments, enabling customization to meet diverse research needs and personal preferences. This user-centric design philosophy ensures that CA-2-HCOMB is accessible to a wide range of users, from seasoned researchers to students just beginning their exploration of protein structures.

## Related Repositories

- [HCOMB-2-CA](https://github.com/ahabegger/HCOMB-2-CA): This repository contains the inverse of CA-2-HCOMB, converting simplified honeycomb structures into a CA Trace.

- [Quantum-Protein-Lattice-Folding](https://github.com/ahabegger/Quantum-Protein-Lattice-Folding): This repository contains the code for the Quantum Protein Lattice Folding project, which uses CA-2-HCOMB to generate simplified structures for quantum computing simulations.

## Types of Simplified Structures

CA-2-HCOMB can transform complex protein structures into simplified models, each providing unique insights and perspectives. All simplification structures have an edge that is one unit long and is composed of convex shapes. These requirements allow the exclusion principle to be followed by making the alpha carbons placed at the vertices not too close to one another. The edges within the models represent the connection between consecutive amino acids. The tool supports the following types of simplified structures:

1. **Square Tiling**: A 2D geometric pattern where squares of identical size are arranged side by side, covering a plane without gaps or overlaps. The 2D model is derived from the XYZ coordinates of the alpha carbon trace in the PDB file by having the amino acids projected onto the 2D plane. The simplification limits movement from one amino acid to another into 4 valid movements represented by [x, y]: [1, 0], [-1, 0], [0, 1], and [0, -1]. 

![square_tiling](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/be712d5b-aebd-4b24-ac7a-dcf0e99d76fc)

2. **Cubic Honeycomb**: A 3D geometric structure of cubes arranged in a continuous pattern. This honeycomb tessellation features cubes that are aligned and stacked in such a way as to fill space without any gaps or overlaps, showcasing perfect symmetry and uniformity. Elevating the representation to three dimensions, the Cubic Honeycomb model extends the alpha carbon trace into a 3D lattice. This model offers a more spatially comprehensive view, portraying how the protein's structure occupies three-dimensional space. The simplification limits movement from one amino acid to another into 6 valid movements represented [x, y, z]: [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], and [0, 0, -1].

![cubic_honeycomb](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/55161819-cbc0-407b-9a09-c8fe663e0dfe)

3. **Triangular Prismatic Honeycomb**: A spatial tessellation formed by stacking triangular prisms in a continuous, repeating pattern. This honeycomb structure is characterized by its uniform, three-sided prisms arranged to fill the space without gaps or overlaps. The simplification limits movement from one amino acid to another into 8 valid movements represented [x, y, z]: [sqrt_3_div_2, 0.5, 0], [-sqrt_3_div_2, 0.5, 0], [0, 1, 0], [sqrt_3_div_2, -0.5, 0], [-sqrt_3_div_2, -0.5, 0], [0, -1, 0], [0, 0, 1], and [0, 0, -1].

![triangular_prismatic_honeycomb](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/0a20ea09-f43b-4c73-a93f-7a6e81c33938)

4. **Tetrahedral-Octahedral Honeycomb**: A complex 3D geometric structure where tetrahedra and octahedra interlock in a repeating pattern. The most complex model in the suite, this structure uses a combination of tetrahedral and octahedral elements to represent the protein's CA Trace in 3D. The simplification limits movement from one amino acid to another into 12 valid movements represented [x, y, z]: [sqrt_2_div_2, sqrt_2_div_2, 0], [sqrt_2_div_2, 0, sqrt_2_div_2], [0, sqrt_2_div_2, sqrt_2_div_2], [-sqrt_2_div_2, -sqrt_2_div_2, 0], [-sqrt_2_div_2, 0, -sqrt_2_div_2], [0, -sqrt_2_div_2, -sqrt_2_div_2], [sqrt_2_div_2, -sqrt_2_div_2, 0], [sqrt_2_div_2, 0, -sqrt_2_div_2], [0, sqrt_2_div_2, -sqrt_2_div_2], [-sqrt_2_div_2, sqrt_2_div_2, 0], [-sqrt_2_div_2, 0, sqrt_2_div_2], and [0, -sqrt_2_div_2, sqrt_2_div_2].

![tetrahedral_octahedral_honeycomb](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/4f8b55d5-1067-4fc9-9fd6-49d04a338fe2)

## Usage

### Installation

To use CA-2-HCOMB, please make sure you have Python installed on your system. Clone or download the repository using one of the following commands: 

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

1. `pdb`: Specify the PDB code or the file path to a PDB file. For example, PDB codes are 101M, 102L, 102M, 103L, 103M, 104M, 105M, 106M, 107L, 107M, 108L, 108M, 109L, 109M, 110L, 110M, 111L, 111M, 112L, 112M, 113L, 114L, etc. The script will prompt you to enter a valid 4-letter PDB code if this argument is not provided.

2. `structure`: Enter the number corresponding to the structure type you wish to create. The script will prompt you to enter a valid structure number if this argument is not provided. The options are:
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

This command processes the PDB code `1A0M`, creates a Cubic Honeycomb structure, visualizes the structure using Matplotlib, generates a report, and outputs the new structure in both XYZ and PDB formats.

![1A0M](https://github.com/ahabegger/PDB-2-Lattice/assets/79123947/aea10afb-1893-4a1f-b26b-e747f70705fa)

### Handling Multiple Chains

The script will warn you if the provided PDB code contains multiple chains. You can override this warning and treat the protein as a single continuous chain.

### Output

Upon successful execution, the script will:
- Print the XYZ coordinates of the created structure.
- Generate visualization plots (if `-v` is used).
- Create a detailed report (if `-r` is used).
- Output the structure in XYZ and PDB formats (if specified).
- Output the TM-Align score of the original and simplified structure.
- Output the RMSD score of the original and simplified structure.

## Potential Improvements

- **Extension to Multi-Chain Support**: Presently, CA-2-HCOMB is limited to handling single-chain structures. Expansion to accommodate multiple chains is a significant avenue for development.

- **Diversification of Test Batteries in Fitting Algorithm**: The current iteration of the fitting algorithm employs a static set of test batteries. Introducing the capability for users to input varied test batteries could significantly enhance the algorithm's adaptability.

- **Refinement of the Tilt Algorithm**: The tilt algorithm is restricted to a specific movement repertoire. Offering a mechanism for users to specify alternative movements would enhance its versatility.

- **Report Generation for Multiple Structures**: The existing version of CA-2-HCOMB supports report generation for only single structures. A feature allowing for concurrently compiling reports for multiple structures would be beneficial.

- **Enhancements in Report Generation**: The clarity and user-friendliness of the generated reports in the current version of CA-2-HCOMB need improvement. Revamping the report generation process to produce more comprehensible and accessible output is a crucial area for enhancement.

## Licensing & Credits

CA-2-HCOMB is released as open-source software under the [MIT License](https://github.com/ahabegger/CA-2-HCOMB/blob/main/LICENSE). This license permits users to modify and distribute the software according to the license's stipulations.

[TM-Align](https://zhanggroup.org/TM-score/) used in Python wrapper TM-Tools was developed by Yang Zhang and Jianyi Yang, and the software version 20210224 is licensed under the GPL v3 license. The TM-Align algorithm is described in the following paper:
- Y. Zhang, J. Skolnick, _Scoring function for automated assessment of protein structure template quality_, Proteins, 57: 702-710 (2004). [Link](https://pubmed.ncbi.nlm.nih.gov/15476259/)
- J. Xu, Y. Zhang, _How significant is a protein structure similarity with TM-score=0.5?_ Bioinformatics, 26, 889-895 (2010). [Link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913670/)

[TM-Tools](https://pypi.org/project/tmtools/) wrapper and modifications are also released under the MIT License.

[Pandas](https://pandas.pydata.org/docs/) is an open source, BSD-licensed dependency.

[NumPy](https://github.com/numpy/numpy/tree/main) is an open source, BSD-licensed dependency.

[Requests](https://pypi.org/project/requests/) uses the Apache Software License (Apache 2.0).

[NGLView](https://pypi.org/project/nglview/) is released under the MIT License.

[Matplotlib](https://pypi.org/project/matplotlib/) is released under the Python Software Foundation License (PSF).

[BioPython](https://pypi.org/project/biopython/) is open source and released under the Biopython License Agreement and BSD License ([See Details](https://github.com/biopython/biopython/blob/master/LICENSE.rst)).

[Dr. Khodakhast Bibak](https://sites.miamioh.edu/khodakhast-bibaks-homepage/?_ga=2.165577279.1008085691.1706802775-453988590.1704227413) advised at each step of the development of this project, and his guidance was invaluable.

## Contact 

I can be contacted by email at my university email habeggaj (at sign) miamioh (dot) edu
