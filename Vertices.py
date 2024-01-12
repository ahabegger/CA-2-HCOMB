import numpy as np
import pandas as pd

import Visualization as plot

# CONVEX UNIFORM HONEYCOMB VERTEX FIGURES

# The vertex figure of a uniform polytope is a polytope whose facets are the
# original polytope. The vertex figure of a uniform polyhedron is a polygon,
# and the vertex figure of a uniform polychoron is a polyhedron.


def get_vertices(shape_code, size):
    # CUBIC HONEYCOMB
    if shape_code == "chon":
        # REQUIREMENTS:
        # (i, j, k)
        # where i, j, k are integers

        points = set()
        # Generate points for the cubic honeycomb
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                for k in range(-size, size + 1):
                    x = i
                    y = j
                    z = k
                    points.add((x, y, z))

        return list(points)

    # TETRAHEDRAL-OCTAHEDRAL HONEYCOMB
    elif shape_code == "octet":
        # REQUIREMENTS:
        # ((sqrt(2)/2) * i, (sqrt(2)/2) * j, (sqrt(2)/2) * k)
        # where i + j + k is even

        points = set()
        # Generate points for the tetrahedral-octahedral honeycomb
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                for k in range(-size, size + 1):
                    if (i + j + k) % 2 == 0:
                        x = (np.sqrt(2) / 2) * i
                        y = (np.sqrt(2) / 2) * j
                        z = (np.sqrt(2) / 2) * k
                        points.add((x, y, z))

        return list(points)

    # TRIANGULAR PRISMATIC HONEYCOMB
    elif shape_code == "triprism":
        # REQUIREMENTS:
        # (+-1/2 + (sqrt(3)/ 2) * i, j + i / 2, k)
        # where i, j, k are integers

        points = set()
        # Generate points for the triangular prismatic honeycomb
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                for k in range(-size, size + 1):
                    x = 0.5 + i * (np.sqrt(3) / 2)
                    y = j + (i / 2)
                    z = k

                    points.add((x, y, z))

        return list(points)

    # HEXAGONAL PRISMATIC HONEYCOMB
    elif shape_code == "hexprism":
        # REQUIREMENTS:
        # (i, j, k)
        # where i, j, k are integers

        points = set()
        # Generate points for the hexagonal prismatic honeycomb
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                for k in range(-size, size + 1):
                    x_pos = 3 * i + 0.5
                    x_neg = 3 * i - 0.5
                    y = j * np.sqrt(3) + (np.sqrt(3) / 2)
                    z = k

                    points.add((x_pos, y, z))
                    points.add((x_neg, y, z))

        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                for k in range(-size, size + 1):
                    x_pos = 3 * i + 1
                    x_neg = 3 * i - 1
                    y = j * np.sqrt(3)
                    z = k

                    points.add((x_pos, y, z))
                    points.add((x_neg, y, z))

        return list(points)


if __name__ == '__main__':
    # 6-Moves
    chon = get_vertices("chon", 2)
    chon = pd.DataFrame(chon, columns=['X', 'Y', 'Z'])
    plot.visualize(chon, title="Cubic Honeycomb", connections=False)

    # 12-Moves
    octet = get_vertices("octet", 2)
    octet = pd.DataFrame(octet, columns=['X', 'Y', 'Z'])
    plot.visualize(octet, title="Tetrahedral-Octahedral Honeycomb", connections=False)

    # 8-Moves
    triprism = get_vertices("triprism", 2)
    triprism = pd.DataFrame(triprism, columns=['X', 'Y', 'Z'])
    plot.visualize(triprism, title="Triangular Prismatic Honeycomb", connections=False)

    # 5-Moves
    hexprism = get_vertices("hexprism", 2)
    hexprism = pd.DataFrame(hexprism, columns=['X', 'Y', 'Z'])
    plot.visualize(hexprism, title="Hexagonal Prismatic Honeycomb", connections=False)

