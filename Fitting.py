"""
Fitting.py
Optimizing a set of movements based on a cost matrix, with the option of using
multiprocessing for parallel execution. The script includes functions to iteratively
refine the movements to achieve the lowest possible cost, utilizing techniques
like local search refinement and testing different combinations of movements, and
it ensures the validity of the final movement set.
"""

import multiprocessing
import time
import numpy as np


def fitting_algorithm(cost_matrix, movements, multiprocess_toggle):
    """
    Creates a set of initial moves and runs the fitting algorithm to optimize the moves
    :param cost_matrix:
    :param movements:
    :param multiprocess_toggle:
    :return: best_moves, best_cost
    """

    best_moves = []
    best_cost = float('inf')

    if not multiprocess_toggle:
        # Run the fitting_movements in parallel
        with multiprocessing.Pool() as pool:
            async_results = []
            for i in range(5):
                initial_moves = [(i % cost_matrix.shape[1])] * cost_matrix.shape[0]
                async_result = pool.apply_async(fitting_movements, (i, initial_moves, cost_matrix, movements))
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
    else:
        # Run the fitting_movements sequentially
        for i in range(5):
            initial_moves = [(i % cost_matrix.shape[1])] * cost_matrix.shape[0]
            moves, final_cost, report = fitting_movements(i, initial_moves, cost_matrix, movements)
            print(report)
            if final_cost < best_cost:
                best_moves = moves
                best_cost = final_cost
            if best_cost == 0:
                break

    # If no valid moves were found, run the failsafe test
    if best_cost == float('inf'):
        initial_moves = [(0 % cost_matrix.shape[1])] * cost_matrix.shape[0]
        best_moves, info1 = test_battery(1, 5, initial_moves, cost_matrix, movements)
        best_moves, info2 = test_battery(2, 3, best_moves, cost_matrix, movements)
        print("FailSafe Test: " + info1 + info2)
        best_cost = get_cost(best_moves, cost_matrix)

    return best_moves, best_cost


def fitting_movements(test_num, moves, cost_matrix, movements):
    """
    Runs a series of Test Batteries to refine the moves and return the best result
    :param test_num:
    :param moves:
    :param cost_matrix:
    :param movements:
    :return: refined_moves, final_cost, report
    """

    start_time = time.time()

    report = f"Test #{test_num}: "
    report += f"Cost={format(get_cost(moves, cost_matrix), '.2f')}|"

    # Refine the moves using local search
    refined_moves = moves
    refined_moves, info2 = test_battery(3, 5, refined_moves, cost_matrix, movements)
    refined_moves, info3 = test_battery(4, 5, refined_moves, cost_matrix, movements)
    refined_moves, info5 = test_battery(5, 2, refined_moves, cost_matrix, movements)
    report += info2 + info3 + info5

    final_cost = get_cost(refined_moves, cost_matrix)
    elapsed_time = time.time() - start_time

    report += f"\nResults #{test_num}: {format(final_cost, '.3f')} in {int(elapsed_time)} seconds"

    return refined_moves, final_cost, report


def test_battery(window_size, num_tests, moves, cost_matrix, movements):
    """
    A Test Battery is a series of tests that are run in sequence to refine the moves.
    :param window_size:
    :param num_tests:
    :param moves:
    :param cost_matrix:
    :param movements:
    :return: lowest_moves, report
    """

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


def run_refinement(window_size, moves, cost_matrix, movements):
    """
    Run the refinement process until the cost no longer changes.
    :param window_size:
    :param moves:
    :param cost_matrix:
    :param movements:
    :return: moves
    """

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
    """
    Refine the moves using local search.
    :param window:
    :param moves:
    :param cost_matrix:
    :param movements:
    :return: moves
    """

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
    """
    Function to recursively find all combinations of cost up to a certain depth (row)
    :param cost_rows:
    :param total_cost:
    :param movements:
    :return:
    """

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
    """
    Get the cost of a given set of moves and cost matrix
    :param moves:
    :param cost_matrix:
    :return: total_cost
    """
    return np.sum(cost_matrix[np.arange(len(moves)), moves])


def is_valid_moves(moves, possible_movements):
    """
    Check if a set of moves is valid based on the possible movements.
    :param moves:
    :param possible_movements:
    :return: validity
    """

    moves = np.array(moves, dtype=int)

    if isinstance(possible_movements, list):
        possible_movements = np.array(possible_movements, dtype=np.float32)

    xyz = np.zeros((len(moves) + 1, 3), dtype=np.float32)
    xyz[1:] = np.cumsum(possible_movements[moves], axis=0)

    for i, point in enumerate(xyz):
        distances = np.linalg.norm(xyz - point, axis=1)
        distances[i] = np.inf  # Ignore the distance of the point to itself
        if np.any(np.isfinite(distances) & (distances < 0.2)):
            return False

    return True
