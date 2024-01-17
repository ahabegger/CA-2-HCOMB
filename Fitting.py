import multiprocessing
import time
import numpy as np

'''
Fitting.py
This Script is used to run the Greedy Lattice Algorithm.
'''


def fitting_algorithm(cost_matrix, movements, multiprocess_toggle):
    # Executes the greedy lattice instance 10 times and returns the best result
    best_moves = []
    best_cost = float('inf')

    # Run the greedy lattice instance in parallel
    with multiprocessing.Pool() as pool:
        async_results = []

        for i in range(5):
            initial_moves = [(i % cost_matrix.shape[1])] * cost_matrix.shape[0]
            async_result = pool.apply_async(greedy_lattice_instance, (i, initial_moves, cost_matrix, movements))
            async_results.append(async_result)

        for async_result in async_results:
            try:
                moves, final_cost, report = async_result.get(timeout=60)
                print(report)
                if final_cost < best_cost:
                    best_moves = moves
                    best_cost = final_cost
                if best_cost == 0:
                    break
            except multiprocessing.TimeoutError:
                print(f"A task exceeded the 60-second limit and was skipped.")
                continue

    # If no valid moves were found, run the failsafe test
    if best_cost == float('inf'):
        initial_moves = [(0 % cost_matrix.shape[1])] * cost_matrix.shape[0]
        best_moves, info1 = test_battery(1, 5, initial_moves, cost_matrix, movements)
        best_moves, info2 = test_battery(2, 3, best_moves, cost_matrix, movements)
        print("FailSafe Test: " + info1 + info2)
        best_cost = get_cost(best_moves, cost_matrix)

    return best_moves, best_cost


def fitting_movements(test_num, moves, cost_matrix, movements):
    start_time = time.time()

    report = f"Test #{test_num}: "
    report += f"Cost={format(get_cost(moves, cost_matrix), '.2f')}|"

    # Refine the moves using local search
    refined_moves = moves
    refined_moves, info2 = test_battery(2, 5, refined_moves, cost_matrix, movements)
    refined_moves, info3 = test_battery(3, 5, refined_moves, cost_matrix, movements)
    refined_moves, info5 = test_battery(5, 2, refined_moves, cost_matrix, movements)
    report += info2 + info3 + info5

    final_cost = get_cost(refined_moves, cost_matrix)
    elapsed_time = time.time() - start_time

    report += f"\nResults #{test_num}: {format(final_cost, '.3f')} in {int(elapsed_time)} seconds"

    return refined_moves, final_cost, report


def test_battery(window_size, num_tests, moves, cost_matrix, movements):
    starting_cost = get_cost(moves, cost_matrix)
    lowest_cost = starting_cost
    lowest_moves = moves.copy()

    report = f'LR{window_size}='

    for i in range(num_tests):
        refined_moves = run_refinement(window_size, moves, cost_matrix, movements)
        refined_cost = get_cost(refined_moves, cost_matrix)
        if refined_cost == 0:
            return refined_moves, report + f"0|"
        elif refined_cost < lowest_cost:
            lowest_cost = get_cost(refined_moves, cost_matrix)
            lowest_moves = refined_moves.copy()

    report += f"{format(lowest_cost - starting_cost, '.2f')}|"

    return lowest_moves, report


def worker(window_size, moves, cost_matrix, movements):
    refined_moves = run_refinement(window_size, moves, cost_matrix, movements)
    refined_cost = get_cost(refined_moves, cost_matrix)
    return refined_moves, refined_cost


def run_refinement(window_size, moves, cost_matrix, movements):
    cost = get_cost(moves, cost_matrix)
    if cost == 0:
        return moves

    change_cost = 1
    while change_cost != 0:
        moves = local_search_refinement(window_size, moves, cost_matrix, movements)
        change_cost = get_cost(moves, cost_matrix) - cost
        cost = get_cost(moves, cost_matrix)

    return moves


def local_search_refinement(window, moves, cost_matrix, movements):
    indices = np.array(range(len(moves) - window + 1))
    randomized_indices = np.random.permutation(indices)

    for i in randomized_indices:
        total_cost = sum(cost_matrix[i + offset, moves[i + offset]] for offset in range(window))

        if total_cost == 0:
            continue

        cost_rows = [cost_matrix[i + offset] for offset in range(window)]
        combinations = find_combinations(cost_rows, total_cost=total_cost, movements=movements)

        if len(combinations) == 0:
            continue

        original_segment = moves[i: i + window].copy()  # Store the original segment
        for combo in combinations:
            moves[i: i + window] = combo  # Update in place
            if is_valid_moves(moves, movements):
                break
            else:
                moves[i: i + window] = original_segment  # Revert if not valid

    return moves


def find_combinations(cost_rows, total_cost, movements):
    # Function to recursively find all combinations of cost up to a certain depth (row)
    def find_combinations_recursive(row, current_cost, current_indices):
        if row == len(cost_rows):
            # Check if the combination is valid and within the cost limit
            if current_cost < total_cost and is_valid_moves(current_indices, movements):
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


def is_valid_moves(moves, possible_movements):
    # Ensure moves is a NumPy array
    moves = np.array(moves, dtype=int)

    # Check if possible_movements is a list of lists or a 2D NumPy array
    if isinstance(possible_movements, list):
        possible_movements = np.array(possible_movements)

    # Initialize the xyz array with the origin and correct size
    xyz = np.zeros((len(moves) + 1, 3), dtype=np.float16)

    # Efficiently compute the cumulative sum of movements
    xyz[1:] = np.cumsum(possible_movements[moves], axis=0, dtype=np.float16)

    _, unique_indices = np.unique(xyz, axis=0, return_index=True)

    return len(unique_indices) == xyz.shape[0]