import matplotlib.pyplot as plt
import pandas as pd


def visualize(xyz, title='Protein Structure'):
    # Convert to DataFrame for easier processing
    df = pd.DataFrame(xyz)

    # Identify unique and repeated points
    is_repeated = df.duplicated(subset=['X', 'Y', 'Z'], keep=False)

    # Create 3D plot
    fig = plt.figure()
    fig.suptitle(title, fontsize=16)
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

