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
    refined_moves = test_battery(2, 5, refined_moves, cost_matrix, movements)
    refined_moves = test_battery(3, 5, refined_moves, cost_matrix, movements)
    refined_moves = test_battery(5, 2, refined_moves, cost_matrix, movements)

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
        print(f"Test {i + 1} for {test_num}")
        refined_moves = run_refinement(test_num, moves, cost_matrix, movements)
        refined_cost = get_cost(refined_moves, cost_matrix)
        if refined_cost == 0:
            return refined_moves
        elif refined_cost < lowest_cost:
            lowest_cost = get_cost(refined_moves, cost_matrix)
            lowest_moves = refined_moves.copy()

    return lowest_moves


def run_refinement(test_num, input_moves, cost_matrix, movements):
    cost = get_cost(input_moves, cost_matrix)
    if cost == 0:
        return input_moves

    change_cost = 1
    output_moves = input_moves.copy()

    while change_cost != 0:
        start_time = time.time()
        print(f'Local Search Refinement {test_num}')
        output_moves = local_search_refinement(test_num, output_moves, cost_matrix, movements)
        change_cost = get_cost(output_moves, cost_matrix) - cost
        print(f"Cost Change: {change_cost}")
        print(f"Cost: {get_cost(output_moves, cost_matrix)}")
        print(f"Total Time: {time.time() - start_time}")
        print('-' * 50)
        cost = get_cost(output_moves, cost_matrix)

    return output_moves


def local_search_refinement(num, moves, cost_matrix, movements):
    indices = np.array(range(len(moves) - num + 1))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        total_cost = sum(cost_matrix[i + offset, moves[i + offset]] for offset in range(num))

        if total_cost == 0:
            continue

        cost_rows = [cost_matrix[i + offset] for offset in range(num)]
        combinations = find_combinations(cost_rows, total_cost=total_cost, movements=movements)

        for combo in combinations:
            new_moves = moves.copy()
            new_moves[i: i + num] = combo
            if xyz_helper.is_valid(xyz_helper.convert_to_xyz(new_moves, movements)):
                moves = new_moves
                break

    return moves


def find_combinations(cost_rows, total_cost, movements):
    # Function to recursively find all combinations of cost up to a certain depth (row)
    def find_combinations_recursive(row, current_cost, current_indices):
        if row == len(cost_rows):
            # Check if the combination is valid and within the cost limit
            if current_cost < total_cost and xyz_helper.is_valid(xyz_helper.convert_to_xyz(current_indices, movements)):
                combinations.append((tuple(current_indices), current_cost))
            return

        for i in range(len(cost_rows[row])):
            # Add the cost of the current cell and call the function recursively for the next row
            find_combinations_recursive(row + 1, current_cost + cost_rows[row][i], current_indices + [i])

    combinations = []
    find_combinations_recursive(0, 0, [])
    combinations.sort(key=lambda x: x[1])

    return [combo for combo, cost in combinations]


def get_cost(moves, cost_matrix):
    return np.sum(cost_matrix[np.arange(len(moves)), moves])
