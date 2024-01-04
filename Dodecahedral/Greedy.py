import numpy as np
import Dodecahedral.XYZ_helper as xyz_helper


def greedy_dodecahederal(moves, cost_df):
    print('-' * 50)
    print('Initial')
    print(f"Moves: {moves}")
    print(f"Cost: {get_cost(moves, cost_df)}")
    print('-' * 50)

    counter = 0
    changes = 0

    for i in np.random.randint(0, len(moves), size=100000):
        # Change the move at index i to a random move
        current_move_cost = cost_df.iloc[i][moves[i]]

        for change_move in range(1, 31):
            change_move_cost = cost_df.iloc[i][change_move]
            if change_move_cost < current_move_cost:
                new_moves = moves.copy()
                new_moves[i] = change_move
                xyz = xyz_helper.convert_to_xyz(new_moves)

                # If the new move is valid, update the moves list and break out of the loop
                if xyz_helper.is_valid(xyz):
                    moves = new_moves
                    changes += 1
                    break

        counter += 1

        # Print out the current state of the lattice every 500 iterations
        if counter % 500 == 0:
            print('-' * 50)
            print(f"Counter: {counter}")
            print(f"Moves: {moves}")
            print(f"Cost: {get_cost(moves, cost_df)}")
            print(f"Changes: {changes}")
            print('-' * 50)

            # If there are no changes in the last 500 iterations, break out of the loop
            if changes == 0:
                break
            else:
                changes = 0


def get_cost(moves, costs):
    num_rows = costs.shape[0]
    total_cost = 0.0

    for i in range(num_rows - 1):
        total_cost += costs.iloc[i][moves[i]]

    return total_cost
