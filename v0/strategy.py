from snake import  direction_after_turn, DIRECTIONS
import numpy as np
from logger import logger as logging

def compute_danger(snake):
    head = snake.positions[0]
    x, y = head
    dirs = [direction_after_turn(snake.dir, "left"), direction_after_turn(snake.dir, "right"), snake.dir]
    tiles = [(x + DIRECTIONS[dir][0], y + DIRECTIONS[dir][1]) for dir in dirs]
    dangers = [0, 0, 0]
    for i, tile in enumerate(tiles):
        if tile in snake.positions or tile[0] < 0 or tile[0] >= snake.board_size or tile[1] < 0 or tile[1] >= snake.board_size:
            dangers[i] = 1
    return dangers


def state_to_index(snake):
    [danger_left, danger_right, danger_center] = compute_danger(snake)
    return danger_left * 2**2 + danger_right * 2 + danger_center

def index_to_state(index):
    danger_center = index % 2
    index //= 2
    danger_right = index % 2
    index //= 2
    danger_left = index % 2
    return danger_left, danger_right, danger_center

def print_Q_table_entry(Q_table, index):
    danger_left, danger_right, danger_center = index_to_state(index)

    state_label = f"danger_left: {danger_left} | danger_right: {danger_right} | danger_center: {danger_center}"
    actions = " | ".join(f"{Q_table[index, j]:.2f}" for j in range(3))
    logging.info(f"{state_label}: {actions}")


def update_Q_table(Q_table, state, action, res, scenari, snake, alpha=0.1, gamma=0.01):
    """Updates the Q-table using the Q-learning algorithm."""
    reward = -1

    if res == False:
        reward = -500

    if res == False:
        return alpha * (reward - Q_table[state][action])
    else:
        next_state = state_to_index(snake)
        return alpha * (reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action])

NSTATES = 2**3
n_actions = 3
Q_table = np.zeros((NSTATES, n_actions))
# We notice that the table could converge really fast to the optimal solution
# But because it gets a -500 when it dies from eating a red apple as well as hitting a wall, sometimes, some path can be not perfectly exact
# We can test it now

# Also the last state is never reached, which make sense
# Because it's rare to have danger left, right and center at the same time

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

