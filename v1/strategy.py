from snake import direction_after_turn, DIRECTIONS
import numpy as np

def _compute_danger(snake):
    head = snake.positions[0]
    x, y = head
    dirs = [direction_after_turn(snake.dir, "left"), direction_after_turn(snake.dir, "right"), snake.dir]
    tiles = [(x + DIRECTIONS[dir][0], y + DIRECTIONS[dir][1]) for dir in dirs]
    dangers = [0, 0, 0]
    for i, tile in enumerate(tiles):
        if tile in snake.positions or tile[0] < 0 or tile[0] >= snake.board_size or tile[1] < 0 or tile[1] >= snake.board_size:
            dangers[i] = 1

    state_index = sum([val * (2**i) for i, val in enumerate(dangers)])
    return state_index

def _compute_red_apple(snake):
    """Returns position of the red apple relative to the snake (None, Left, Right, Center)."""
    head = snake.positions[0]
    if not snake.red_apple_positions:
        return 0  # No red apple

    red_apple = list(snake.red_apple_positions)[0]  # There is only one red apple
    directions = [direction_after_turn(snake.dir, "left"),
                  direction_after_turn(snake.dir, "right"),
                  snake.dir]

    tiles = [(head[0] + DIRECTIONS[d][0], head[1] + DIRECTIONS[d][1]) for d in directions]

    if red_apple == tiles[0]:  # Left
        return 1
    elif red_apple == tiles[1]:  # Right
        return 2
    elif red_apple == tiles[2]:  # Center
        return 3
    return 0  # No red apple

def _compute_green_apple(snake):
    """Returns the position of a green apple relative to the snake (before an obstacle)."""
    head = snake.positions[0]
    x, y = head
    possible_states = [0] * 3  # [Left, Right, Center]

    for apple in snake.green_apple_positions:
        dx, dy = apple[0] - x, apple[1] - y

        # Check if it's in line with the snake's movement
        if (dx == 0 and dy != 0) or (dx != 0 and dy == 0):
            direction = None
            if (dy < 0 and snake.dir == 3) or (dy > 0 and snake.dir == 1):  # Left/Right
                direction = "left" if dy < 0 else "right"
            elif (dx < 0 and snake.dir == 0) or (dx > 0 and snake.dir == 2):  # Up/Down
                direction = "left" if dx < 0 else "right"

            if direction:
                index = 0 if direction == "left" else 1
                possible_states[index] = 1
            else:
                possible_states[2] = 1  # Center

    state_index = sum([val * (2**i) for i, val in enumerate(possible_states)])

    return state_index

def state_to_index(snake):
    """Returns a unique index for the state representation."""
    danger = _compute_danger(snake)
    red_apple = _compute_red_apple(snake)
    green_apple = _compute_green_apple(snake)

    return danger * (4 * 7) + red_apple * 7 + green_apple

def print_Q_table(Q_table):
    """Prints the Q-table in a readable format without affecting performance."""

    DANGER_LABELS = ["Safe", "Left", "Right", "Center", "Left+Right", "Left+Center", "Right+Center", "All"]
    RED_APPLE_LABELS = ["No Red", "Left", "Right", "Center"]
    GREEN_APPLE_LABELS = ["No Green", "Left", "Right", "Center", "Left+Right", "Left+Center", "Right+Center"]

    print("\nQ-table:")
    for state in range(NSTATES):
        danger = state // (4 * 7)
        red = (state % (4 * 7)) // 7
        green = (state % 7)

        state_label = f"{DANGER_LABELS[danger]:<6} | {RED_APPLE_LABELS[red]:<7} | {GREEN_APPLE_LABELS[green]:<12}"
        row = " | ".join(f"{Q_table[state, j]:.2f}" for j in range(n_actions))
        print(f"{state_label}: {row}")

def update_Q_table(Q_table, state, action, res, scenari, snake, alpha=0.1, gamma=0.9):
    """Updates the Q-table using the Q-learning algorithm."""
    reward = -1
    if res == False and scenari != "red":
        reward = -500
    else:
        if scenari == "red":
            reward = -10
        elif scenari == "green":
            reward = 10

    if res == False:
        return alpha * (reward - Q_table[state][action])
    else:
        next_state = state_to_index(snake)
        return alpha * (reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action])



NSTATES = 224  # 8 (Danger) * 4 (Red Apple) * 7 (Green Apple)
n_actions = 3  # Left, Right, Forward

Q_table = np.zeros((NSTATES, n_actions))
