from PDB2Backbone import create_backbone
from Structures import create_lattice
import pandas as pd
from matplotlib import pyplot as plt

'''
main.py
This Script takes a PDB code and a structure type and creates a report containing the original PDB file, the modified
PDB file, and the diagrams of both.
'''


def user_input():
    print("Sample PDB Codes are 1A0M, 1A1M, 1A2M, 1A3M, 1A4M, "
          "1A5M, 1A6M, 1A7M, 1A8M, 1A9M, 1B0M, 1B1M, 1B2M, 1B3M, 1B4M")
    user_pdb = input("Input 4-Letter PDB Code: ")

    print("Input the Number for the Structure you want to create:")
    print("1  = CA BACKBONE")
    print("4  = SQUARE TILING")
    print("6  = CUBIC HONEYCOMB")
    print("8  = TRIANGULAR PRISMATIC HONEYCOMB")
    print("12 = TETRAHEDRAL-OCTAHEDRAL HONEYCOMB")

    structure = input("Input Structure: ")

    return user_pdb, structure


def menu(pdb_code, structure, visualize=True):
    if structure == "1":  # CA Backbone Structure
        xyz, cost, time = create_backbone(pdb_code), 0, 0
        if visualize:
            plot_structure(xyz[['X', 'Y', 'Z']], title="CA Backbone Structure")
        #  create_report(pdb_code, xyz, "CA Backbone Structure")
    else:
        xyz, cost, time = create_lattice(int(structure), pdb_code)
        if visualize:
            plot_structure(xyz, title=f"{structure} Move Lattice for {pdb_code}")
        #  create_report(pdb_code, xyz, f"{structure} Lattice Structure")

    return cost, time


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

    return None


def testing(pdb_code):
    structures = ["1", "4", "6", "8", "12"]
    costs = []
    times = []

    for structure in structures:
        cost, time = menu(pdb_code, structure, visualize=False)
        costs.append(cost)
        times.append(time)

    print("Costs: ", costs)
    print("Times: ", times)
    print("Total Cost: ", sum(costs))
    print("Total Time: ", sum(times))


if __name__ == '__main__':
    # pdb_code, structure = user_input()

    # structure = "4"
    pdb = "1A2M"

    menu(pdb, "12", visualize=True)
