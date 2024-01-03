import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import mplcursors


def visualize(lowest_xyz, amino_info):
    # Convert to DataFrame for easier processing
    df = pd.DataFrame(lowest_xyz)

    # Add the amino acid information
    amino_df = amino_info[['ID', 'Amino Acid']]  # Extract the ID and Amino Acid columns

    # Merge the amino acid information with the coordinate data
    df = pd.concat([df, amino_df], axis=1)

    # Identify unique and repeated points
    is_repeated = df.duplicated(subset=['X', 'Y', 'Z'], keep=False)

    # Create 3D plot
    fig = plt.figure()
    fig.suptitle('One Dimensional Cubic Lattice', fontsize=16)
    ax = fig.add_subplot(projection='3d')

    # Plot all points as a line plot to maintain the original order
    ax.plot3D(df['X'], df['Y'], df['Z'], color='blue', label='Line Connection')

    # Overplot unique points in green and repeated points in red
    ax.scatter(df.loc[~is_repeated, 'X'], df.loc[~is_repeated, 'Y'], df.loc[~is_repeated, 'Z'],
               color='green',
               label='Unique Points')
    ax.scatter(df.loc[is_repeated, 'X'], df.loc[is_repeated, 'Y'], df.loc[is_repeated, 'Z'],
               color='red',
               label='Repeated Points')

    # Show plot
    plt.legend()
    plt.show()

    return None

