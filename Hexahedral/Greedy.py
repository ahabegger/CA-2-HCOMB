import time
import numpy as np
import Hexahedral.XYZ_helper as xyz_helper


def greedy_hexahedral(moves, cost_df):
    cost_matrix = cost_df.to_numpy()
    cost_matrix = np.insert(cost_matrix, 0, 100, axis=1)

    print('-' * 50)
    print("Greedy Hexahedral (6 Move) Lattice")
    print(f"Initial Moves: {moves}")
    print(f"Initial Cost: {get_cost(moves, cost_matrix)}")
    print('-' * 50)

    start_time = time.time()
    num_moves = len(moves)
    changes = 0

    for iteration in range(1, 10000):
        # Pick a random move
        i = np.random.randint(0, num_moves)

        # Find all moves with a smaller cost than the current move
        current_move = moves[i]
        current_move_cost = cost_matrix[i, current_move]
        smaller_costs = np.where(cost_matrix[i] < current_move_cost)[0]

        if smaller_costs.size != 0:
            new_move = np.random.choice(smaller_costs)
            new_moves = moves.copy()
            new_moves[i] = new_move

            # If the new move is valid, update the moves list and break out of the loop
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves)):
                moves = new_moves
                changes += 1

        if iteration % 1000 == 0:
            print(f"Iteration: {iteration}")
            print(f"Moves: {moves}")
            print(f"Cost: {get_cost(moves, cost_matrix)}")
            print(f"Changes: {changes}")
            print('-' * 50)

            if changes == 0:
                break
            changes = 0

    final_cost = get_cost(moves, cost_matrix)
    print(f"--- {time.time() - start_time} seconds ---")
    print(f"--- {final_cost} cost ---")

    return moves, final_cost


def get_cost(moves, cost_matrix):
    return np.sum(cost_matrix[np.arange(len(moves)), moves])
