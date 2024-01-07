import time
import numpy as np
import XYZHelper as xyz_helper


def greedy_lattice(cost_df, movements):
    # Executes the greedy lattice instance 10 times and returns the best result
    best_moves = []
    best_cost = float('inf')
    start_time = time.time()

    for i in range(1):
        # Initialize the moves list with the first move being the first column of the cost_df
        initial_moves = [(i % cost_df.shape[1]) + 1] * cost_df.shape[0]

        # Run the greedy lattice instance
        moves, final_cost = greedy_lattice_instance(initial_moves, cost_df, movements)

        # If the final cost is better than the current best cost, update the best moves and best cost
        if final_cost < best_cost:
            best_moves = moves
            best_cost = final_cost
        if best_cost == 0:
            break

    return best_moves, best_cost, time.time() - start_time


def greedy_lattice_instance(moves, cost_df, movements):
    start_time = time.time()
    cost_matrix = cost_df.to_numpy()
    cost_matrix = np.insert(cost_matrix, 0, 1000, axis=1)

    print('-' * 50)
    print(f"Initial Moves: {moves}")
    print(f"Initial Cost: {get_cost(moves, cost_matrix)}")
    print('-' * 50)

    cost = get_cost(moves, cost_matrix)

    test_options = [[1, 2]]
    index = np.random.choice(len(test_options))
    for test in test_options[index]:
        if cost != 0:
            moves = run_refinement(test, moves, cost_matrix, movements)

    final_cost = get_cost(moves, cost_matrix)
    elapsed_time = time.time() - start_time
    print(f"--- Final Moves: {moves}")
    print(f"--- {elapsed_time} seconds")
    print(f"--- {final_cost} cost")

    return moves, final_cost


def run_refinement(test_num, moves, cost_matrix, movements):
    cost = get_cost(moves, cost_matrix)
    change_cost = 1

    if test_num == 1:
        while change_cost != 0:
            print('Local Search Refinement 3')
            moves = local_search_refinement_3(moves, cost_matrix, movements)
            change_cost = cost - get_cost(moves, cost_matrix)
            print(f"Cost Change: -{change_cost}")
            print('-' * 50)
            cost = get_cost(moves, cost_matrix)
    elif test_num == 2:
        while change_cost != 0:
            print('Local Search Refinement 5')
            moves = local_search_refinement_5(moves, cost_matrix, movements)
            change_cost = cost - get_cost(moves, cost_matrix)
            print(f"Cost Change: -{change_cost}")
            print('-' * 50)
            cost = get_cost(moves, cost_matrix)
    elif test_num == 3:
        while change_cost != 0:
            print('Local Search Refinement 7')
            moves = local_search_refinement_7(moves, cost_matrix, movements)
            change_cost = cost - get_cost(moves, cost_matrix)
            print(f"Cost Change: -{change_cost}")
            print('-' * 50)
            cost = get_cost(moves, cost_matrix)

    return moves


def local_search_refinement_3(moves, cost_matrix, movements):
    indices = np.array(range(1, len(moves) - 1))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        total_cost = (cost_matrix[i, moves[i]] +
                      cost_matrix[i + 1, moves[i + 1]] +
                      cost_matrix[i - 1, moves[i - 1]])
        cost_above = cost_matrix[i + 1]
        cost_below = cost_matrix[i - 1]
        cost_current = cost_matrix[i]

        combinations = find_combinations_3(cost_above, cost_below, cost_current, total_cost)
        for combo in combinations:
            new_moves = moves.copy()
            new_moves[i - 1] = combo[0]
            new_moves[i] = combo[1]
            new_moves[i + 1] = combo[2]
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves, movements)):
                if get_cost(new_moves, cost_matrix) < get_cost(moves, cost_matrix):
                    moves = new_moves

    return moves


def find_combinations_3(cost_above, cost_below, cost_current, total_cost):
    if total_cost == 0:
        return []

    # List to store valid combinations
    valid_combinations = []

    # Iterate through each combination of indices
    for i in range(len(cost_above)):
        for j in range(len(cost_below)):
            for k in range(len(cost_current)):
                # Check if the sum of the selected elements is less than total_cost
                if cost_above[i] + cost_below[j] + cost_current[k] < total_cost:
                    valid_combinations.append((j, k, i))

    return valid_combinations


def local_search_refinement_5(moves, cost_matrix, movements):
    indices = np.array(range(2, len(moves) - 2))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        total_cost = sum(cost_matrix[i + offset, moves[i + offset]] for offset in range(-2, 3))

        if total_cost == 0:
            continue

        cost_above_1 = cost_matrix[i + 1]
        cost_above_2 = cost_matrix[i + 2]
        cost_below_1 = cost_matrix[i - 1]
        cost_below_2 = cost_matrix[i - 2]
        cost_current = cost_matrix[i]

        combinations = find_combinations_5(cost_above_1, cost_above_2, cost_below_1, cost_below_2, cost_current,
                                           total_cost)
        for combo in combinations:
            new_moves = moves.copy()
            new_moves[i - 2] = combo[0]
            new_moves[i - 1] = combo[1]
            new_moves[i] = combo[2]
            new_moves[i + 1] = combo[3]
            new_moves[i + 2] = combo[4]
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves, movements)):
                if get_cost(new_moves, cost_matrix) < get_cost(moves, cost_matrix):
                    moves = new_moves

    return moves


def find_combinations_5(cost_above_1, cost_above_2, cost_below_1, cost_below_2, cost_current, total_cost):
    valid_combinations = []
    for a in range(len(cost_above_2)):
        for b in range(len(cost_above_1)):
            for c in range(len(cost_current)):
                for d in range(len(cost_below_1)):
                    for e in range(len(cost_below_2)):
                        if (cost_above_2[a] + cost_above_1[b] + cost_current[c]
                                + cost_below_1[d] + cost_below_2[e] < total_cost):
                            valid_combinations.append((e, d, c, b, a))

    return valid_combinations


def local_search_refinement_7(moves, cost_matrix, movements):
    indices = np.array(range(3, len(moves) - 3))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        total_cost = sum(cost_matrix[i + offset, moves[i + offset]] for offset in range(-3, 4))

        if total_cost == 0:
            continue

        cost_above_1 = cost_matrix[i + 1]
        cost_above_2 = cost_matrix[i + 2]
        cost_above_3 = cost_matrix[i + 3]
        cost_below_1 = cost_matrix[i - 1]
        cost_below_2 = cost_matrix[i - 2]
        cost_below_3 = cost_matrix[i - 3]
        cost_current = cost_matrix[i]

        combinations = find_combinations_7(cost_above_1, cost_above_2, cost_above_3,
                                           cost_below_1, cost_below_2, cost_below_3,
                                           cost_current, total_cost)
        for combo in combinations:
            new_moves = moves.copy()
            new_moves[i - 3] = combo[0]
            new_moves[i - 2] = combo[1]
            new_moves[i - 1] = combo[2]
            new_moves[i] = combo[3]
            new_moves[i + 1] = combo[4]
            new_moves[i + 2] = combo[5]
            new_moves[i + 3] = combo[6]
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves, movements)):
                if get_cost(new_moves, cost_matrix) < get_cost(moves, cost_matrix):
                    moves = new_moves

    return moves


def find_combinations_7(cost_above_1, cost_above_2, cost_above_3, cost_below_1, cost_below_2, cost_below_3,
                        cost_current, total_cost):
    valid_combinations = []
    for a in range(len(cost_above_3)):
        for b in range(len(cost_above_2)):
            for c in range(len(cost_above_1)):
                for d in range(len(cost_current)):
                    for e in range(len(cost_below_1)):
                        for f in range(len(cost_below_2)):
                            for g in range(len(cost_below_3)):
                                if (cost_above_3[a] + cost_above_2[b] + cost_above_1[c] +
                                        cost_current[d] + cost_below_1[e] + cost_below_2[f] +
                                        cost_below_3[g] < total_cost):
                                    valid_combinations.append((g, f, e, d, c, b, a))

    return valid_combinations


def get_cost(moves, cost_matrix):
    return np.sum(cost_matrix[np.arange(len(moves)), moves])
