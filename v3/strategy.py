import numpy as np
from logger import logger as logging




def state_to_index(snake):
    """Returns a unique index for the state representation."""
    row = snake.positions[0][0]
    col = snake.positions[0][1]

    return row * 10 + col

def index_to_state(index):
    row = index // 10
    col = index % 10

    return row, col

def print_Q_table_entry(Q_table, index):
    row, col = index_to_state(index)

    state_label = f"row: {row} | col: {col}"
    actions = " | ".join(f"{Q_table[index, j]:.2f}" for j in range(n_actions))
    logging.info(f"{state_label}: {actions}")

def print_Q_table(Q_table):
    """Prints the Q-table in a readable format without affecting performance."""

    print("\nQ-table:")
    for state in range(NSTATES):
        print_Q_table_entry(Q_table, state)

hamiltonian_cycle = [
    (0, 0),
    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
    (9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1),
    (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
    (9, 3), (8, 3), (7, 3), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3),
    (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
    (9, 5), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5),
    (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
    (9, 7), (8, 7), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7),
    (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
    (9, 9), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9),
    (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1)
]

def update_Q_table(Q_table, state, action, res, scenari, snake, alpha=0.1, gamma=0.01):
    """Updates the Q-table using the Q-learning algorithm."""
    reward = -300


    if update_Q_table.previous_pos:
        hamiltonian_idx = hamiltonian_cycle.index(snake.positions[0])
        if hamiltonian_idx == (hamiltonian_cycle.index(update_Q_table.previous_pos) + 1) % len(hamiltonian_cycle):
            reward = 100
    update_Q_table.previous_pos = snake.positions[0]

    if res == False:
        return alpha * (reward - Q_table[state][action])
    else:
        next_state = state_to_index(snake)
        return alpha * (reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action])

update_Q_table.previous_pos = None


NSTATES = 100  # 8 (Danger) * 4 (Red Apple) * 7 (Green Apple)
n_actions = 4  # UP, LEFT, DOWN, RIGHT

Q_table = np.zeros((NSTATES, n_actions))




def print_learning_progress(q_table, verbose = "minimal"):
    visited_states = 0
    taken_actions = 0
    state_count = 0
    for state in range(NSTATES):
        state_count += 1
        taken_actions += np.count_nonzero(q_table[state])
        if np.any(q_table[state]):
            visited_states += 1

        if verbose == "full":
            print_Q_table_entry(q_table, state)
        if verbose == "medium" and np.any(q_table[state] == 0):
            print_Q_table_entry(q_table, state)


    logging.info(f"Learning progress (state): {visited_states}/{state_count} ({(visited_states/state_count * 100):.2f} %)")
    logging.info(f"Learning progress (actions): {taken_actions}/{state_count * n_actions} ({(taken_actions/(state_count * 3) * 100):.2f} %)")
