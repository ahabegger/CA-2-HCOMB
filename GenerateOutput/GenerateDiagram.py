import os

import nglview
import pandas as pd
from matplotlib import pyplot as plt

'''
GenerateDiagram.py
This Script takes a PDB code and a DataFrame containing the new coordinates of the protein backbone and creates a
report containing the original PDB file, the modified PDB file, and the diagrams of both.
'''


def plot_structure(xyz, title='Protein Structure'):
    # Convert to DataFrame for easier processing
    df = pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])

    # Create 3D plot
    fig = plt.figure()
    fig.suptitle(title, fontsize=16)
    ax = fig.add_subplot(projection='3d')

    # Plot points
    ax.scatter(df['X'], df['Y'], df['Z'], color='green', label='Points')

    # Draw connections
    ax.plot3D(df['X'], df['Y'], df['Z'], color='blue', label='Line Connection')

    # Show plot
    plt.legend()
    plt.show()


def create_nglview(pdb_file):
    view = nglview.show_structure_file(pdb_file)
    nglview.write_html(f'{pdb_file.split("/")[2].split(".")[0]}_diagram.html', view)


def get_nglview_html(filename):
    diagram = ""
    with open(filename) as file:
        for line in file:
            diagram += line
    diagram = diagram.split("body>")[1][:-2]
    os.remove(filename)
    return diagram


def plot_structure_to_image(xyz, filename, title='Protein Structure'):
    # Convert to DataFrame for easier processing
    df = pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])

    # Create 3D plot
    fig = plt.figure()
    fig.suptitle(title, fontsize=16)
    ax = fig.add_subplot(projection='3d')

    # Plot points
    ax.scatter(df['X'], df['Y'], df['Z'], color='green', label='Points')

    # Draw connections
    ax.plot3D(df['X'], df['Y'], df['Z'], color='blue', label='Line Connection')

    # Save the figure as a PNG file
    plt.savefig(filename, bbox_inches='tight')

    plt.close(fig)

    reference_filename = "Plots/" + filename.split('/')[-1]

    return f"<img src=\"{reference_filename}\" alt=\"{title}\">\n"
