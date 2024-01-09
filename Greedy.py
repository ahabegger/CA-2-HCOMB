# Import Outside Statements
import time
import numpy as np

# Import Local Statements
import XYZHelper as xyz_helper

'''
Greedy.py
This Script is used to run the Greedy Lattice Algorithm.
'''


def greedy_lattice(cost_df, movements):
    # Executes the greedy lattice instance 10 times and returns the best result
    best_moves = []
    best_cost = float('inf')
    start_time = time.time()

    for i in range(5):
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
    print(f"TESTING: {len(movements)} - MOVE LATTICE")
    print(f"Initial Moves: {moves}")
    print(f"Initial Cost: {get_cost(moves, cost_matrix)}")
    print('-' * 50)

    refined_moves = moves.copy()

    # Refine the moves using local search
    #refined_moves = test_battery(0, 5, refined_moves, cost_matrix, movements)
    refined_moves = test_battery(1, 5, refined_moves, cost_matrix, movements)
    refined_moves = test_battery(2, 2, refined_moves, cost_matrix, movements)

    final_cost = get_cost(refined_moves, cost_matrix)
    elapsed_time = time.time() - start_time
    print(f"--- Final Moves: {refined_moves}")
    print(f"--- {elapsed_time} seconds")
    print(f"--- {final_cost} cost")

    return refined_moves, final_cost


def test_battery(test_num, num_tests, moves, cost_matrix, movements):
    lowest_cost = get_cost(moves, cost_matrix)
    lowest_moves = moves.copy()

    for i in range(num_tests):
        print(f"Test {i + 1} for {test_num * 2 + 1}")
        refined_moves = run_refinement(test_num, moves, cost_matrix, movements)
        if get_cost(refined_moves, cost_matrix) < lowest_cost:
            lowest_cost = get_cost(refined_moves, cost_matrix)
            lowest_moves = refined_moves.copy()

    return lowest_moves


def run_refinement(test_num, input_moves, cost_matrix, movements):
    cost = get_cost(input_moves, cost_matrix)
    change_cost = 1

    output_moves = input_moves.copy()
    if test_num == 0:
        while change_cost != 0:
            start_time = time.time()
            print('Local Search Refinement 1')
            output_moves = local_search_refinement_1(output_moves, cost_matrix, movements)
            change_cost = get_cost(output_moves, cost_matrix) - cost
            print(f"Cost Change: {change_cost}")
            print(f"Cost: {get_cost(output_moves, cost_matrix)}")
            print(f"Total Time: {time.time() - start_time}")
            print('-' * 50)
            cost = get_cost(output_moves, cost_matrix)
    elif test_num == 1:
        while change_cost != 0:
            start_time = time.time()
            print('Local Search Refinement 3')
            output_moves = local_search_refinement_3(output_moves, cost_matrix, movements)
            change_cost = get_cost(output_moves, cost_matrix) - cost
            print(f"Cost Change: {change_cost}")
            print(f"Cost: {get_cost(output_moves, cost_matrix)}")
            print(f"Total Time: {time.time() - start_time}")
            print('-' * 50)
            cost = get_cost(output_moves, cost_matrix)
    elif test_num == 2:
        while change_cost != 0:
            start_time = time.time()
            print('Local Search Refinement 5')
            output_moves = local_search_refinement_5(output_moves, cost_matrix, movements)
            change_cost = get_cost(output_moves, cost_matrix) - cost
            print(f"Cost Change: {change_cost}")
            print(f"Cost: {get_cost(output_moves, cost_matrix)}")
            print(f"Total Time: {time.time() - start_time}")
            print('-' * 50)
            cost = get_cost(output_moves, cost_matrix)
    elif test_num == 3:
        while change_cost != 0:
            start_time = time.time()
            print('Local Search Refinement 7')
            output_moves = local_search_refinement_7(output_moves, cost_matrix, movements)
            change_cost = get_cost(output_moves, cost_matrix) - cost
            print(f"Cost Change: {change_cost}")
            print(f"Cost: {get_cost(output_moves, cost_matrix)}")
            print(f"Total Time: {time.time() - start_time}")
            print('-' * 50)
            cost = get_cost(output_moves, cost_matrix)

    return output_moves


def local_search_refinement_1(moves, cost_matrix, movements):
    indices = np.array(range(0, len(moves)))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        cost = cost_matrix[i, moves[i]]
        if cost == 0:
            continue

        cost_rows = cost_matrix[i]
        combinations = sorted_indices_below_threshold(cost_rows, cost)

        for combo in combinations:
            new_moves = moves.copy()
            new_moves[i] = combo
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves, movements)):
                moves = new_moves
                break

    return moves


def sorted_indices_below_threshold(arr, threshold):
    arr = np.array(arr)
    # Filter the array to include only elements less than the threshold
    filtered_indices = np.where(arr < threshold)[0]

    # Sort these indices based on the values in the original array
    sorted_indices = filtered_indices[np.argsort(arr[filtered_indices])]

    return sorted_indices.tolist()


def local_search_refinement_3(moves, cost_matrix, movements):
    indices = np.array(range(1, len(moves) - 1))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        total_cost = sum(cost_matrix[i + offset, moves[i + offset]] for offset in range(-1, 2))

        if total_cost == 0:
            continue

        cost_rows = [cost_matrix[i + offset] for offset in [-1, 0, 1]]
        combinations = find_combinations_3(*cost_rows, total_cost=total_cost, movements=movements)

        for combo in combinations:
            new_moves = moves.copy()
            new_moves[i - 1: i + 2] = combo
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves, movements)):
                moves = new_moves
                break

    return moves


def find_combinations_3(cost_below, cost_current, cost_above, total_cost, movements):
    # List to store valid combinations
    combinations = []

    # Iterate through each combination of indices
    for i in range(len(cost_above)):
        for j in range(len(cost_current)):
            for k in range(len(cost_below)):
                combination_cost = cost_above[i] + cost_current[j] + cost_below[k]
                if combination_cost < total_cost:
                    if xyz_helper.is_valid(xyz_helper.convert_to_xyz([k, j, i], movements)):
                        combinations.append(((k, j, i), combination_cost))

    # Sort combinations by cost
    combinations.sort(key=lambda x: x[1])

    return [combo for combo, cost in combinations]


def local_search_refinement_5(moves, cost_matrix, movements):
    indices = np.array(range(2, len(moves) - 2))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        total_cost = sum(cost_matrix[i + offset, moves[i + offset]] for offset in range(-2, 3))

        if total_cost == 0:
            continue

        cost_rows = [cost_matrix[i + offset] for offset in [-2, -1, 0, 1, 2]]
        combinations = find_combinations_5(*cost_rows, total_cost=total_cost, movements=movements)

        for combo in combinations:
            new_moves = moves.copy()
            new_moves[i - 2: i + 3] = combo
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves, movements)):
                moves = new_moves
                break

    return moves


def find_combinations_5(cost_below_2, cost_below_1, cost_current, cost_above_1, cost_above_2, total_cost, movements):
    combinations = []
    for a in range(len(cost_above_2)):
        for b in range(len(cost_above_1)):
            for c in range(len(cost_current)):
                for d in range(len(cost_below_1)):
                    for e in range(len(cost_below_2)):
                        combination_cost = cost_above_2[a] + cost_above_1[b] + cost_current[c] + cost_below_1[d] + \
                                           cost_below_2[e]
                        if combination_cost < total_cost:
                            if xyz_helper.is_valid(xyz_helper.convert_to_xyz([e, d, c, b, a], movements)):
                                combinations.append(((e, d, c, b, a), combination_cost))

    # Sort combinations by cost
    combinations.sort(key=lambda x: x[1])

    return [combo for combo, cost in combinations]


def local_search_refinement_7(moves, cost_matrix, movements):
    indices = np.array(range(3, len(moves) - 3))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        total_cost = sum(cost_matrix[i + offset, moves[i + offset]] for offset in range(-3, 4))

        if total_cost == 0:
            continue

        cost_rows = [cost_matrix[i + offset] for offset in [-3, -2, -1, 0, 1, 2, 3]]
        combinations = find_combinations_7(*cost_rows, total_cost=total_cost, movements=movements)

        for combo in combinations:
            new_moves = moves.copy()
            new_moves[i - 3: i + 4] = combo
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves, movements)):
                moves = new_moves
                break

    return moves


def find_combinations_7(cost_below_3, cost_below_2, cost_below_1, cost_current, cost_above_1, cost_above_2,
                        cost_above_3, total_cost, movements):
    combinations = []
    for a in range(len(cost_above_3)):
        for b in range(len(cost_above_2)):
            for c in range(len(cost_above_1)):
                for d in range(len(cost_current)):
                    for e in range(len(cost_below_1)):
                        for f in range(len(cost_below_2)):
                            for g in range(len(cost_below_3)):
                                combination_cost = (cost_above_3[a] + cost_above_2[b] + cost_above_1[c] +
                                                    cost_current[d] + cost_below_1[e] + cost_below_2[f] +
                                                    cost_below_3[g])
                                if combination_cost < total_cost:
                                    if xyz_helper.is_valid(xyz_helper.convert_to_xyz([g, f, e, d, c, b, a], movements)):
                                        combinations.append(((g, f, e, d, c, b, a), combination_cost))

    # Sort combinations by cost
    combinations.sort(key=lambda x: x[1])

    return [combo for combo, cost in combinations]


def get_cost(moves, cost_matrix):
    return np.sum(cost_matrix[np.arange(len(moves)), moves])
