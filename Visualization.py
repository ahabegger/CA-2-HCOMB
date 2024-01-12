# Import Outside Libraries
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def visualize(xyz, title='Protein Structure', connections=True):
    # Convert to DataFrame for easier processing
    df = pd.DataFrame(xyz, columns=['X', 'Y', 'Z'])

    # Create 3D plot
    fig = plt.figure()
    fig.suptitle(title, fontsize=16)
    ax = fig.add_subplot(projection='3d')

    # Plot points
    ax.scatter(df['X'], df['Y'], df['Z'], color='green', label='Points')

    # Draw connections
    if connections:
        ax.plot3D(df['X'], df['Y'], df['Z'], color='blue', label='Line Connection')
    else:
        tolerance = 0.1
        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                # Calculate the distance between points
                point1 = df.iloc[i]
                point2 = df.iloc[j]
                distance = np.linalg.norm(point1 - point2)

                # Draw a line if the distance is close to 1 (within the specified tolerance)
                if abs(distance - 1) <= tolerance:
                    ax.plot([point1['X'], point2['X']],
                            [point1['Y'], point2['Y']],
                            [point1['Z'], point2['Z']],
                            color='blue', linewidth=0.5)

    # Show plot
    plt.legend()
    plt.show()

    return None
