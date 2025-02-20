from snake import direction_after_turn, DIRECTIONS, UP, DOWN, LEFT, RIGHT
import numpy as np
from logger import logger as logging


def _compute_danger(snake):
    head = snake.positions[0]
    x, y = head
    dirs = [direction_after_turn(snake.dir, "left"), direction_after_turn(snake.dir, "right"), snake.dir]
    logging.debug("Dirs: {dirs}")
    tiles = [(x + DIRECTIONS[dir][0], y + DIRECTIONS[dir][1]) for dir in dirs]
    logging.debug(f"Tiles: {tiles}")
    dangers = [0, 0, 0]
    for i, tile in enumerate(tiles):
        if tile in snake.positions or tile[0] < 0 or tile[0] >= snake.board_size or tile[1] < 0 or tile[1] >= snake.board_size:
            dangers[i] = 1

    logging.debug(f"Dangers: {dangers}")

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

    logging.debug(f"Red apple: {red_apple}")
    logging.debug(f"Tiles: {tiles}")
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

    logging.debug(f"Green apples: {snake.green_apple_positions}")

    for apple in snake.green_apple_positions:
        dx, dy = apple[0] - x, apple[1] - y
        logging.debug(f"Apple: {apple} dx, dy: {dx, dy}")

        # Check if it's in line with the snake's movement
        if (dx == 0 and dy != 0) or (dx != 0 and dy == 0):
            blocked = False
            tmp_x, tmp_y = x, y
            while (tmp_x, tmp_y) != apple:
                tmp_x += (dx > 0) - (dx < 0)
                tmp_y += (dy > 0) - (dy < 0)
                if (tmp_x, tmp_y) in snake.positions or (tmp_x, tmp_y) in snake.red_apple_positions:
                    blocked = True
                    break

            direction = None
            if not blocked:
                if dy < 0:
                    if snake.dir == UP:
                        direction = "left"
                    elif snake.dir == DOWN:
                        direction = "right"
                    elif snake.dir == LEFT:
                        direction = "center"
                elif dy > 0:
                    if snake.dir == UP:
                        direction = "right"
                    elif snake.dir == DOWN:
                        direction = "left"
                    elif snake.dir == RIGHT:
                        direction = "center"
                elif dx < 0:
                    if snake.dir == LEFT:
                        direction = "right"
                    elif snake.dir == RIGHT:
                        direction = "left"
                    elif snake.dir == UP:
                        direction = "center"
                elif dx > 0:
                    if snake.dir == LEFT:
                        direction = "left"
                    elif snake.dir == RIGHT:
                        direction = "right"
                    elif snake.dir == DOWN:
                        direction = "center"

            if direction:
                possible_states[["left", "right", "center"].index(direction)] = 1
    logging.debug(f"Possible states: {possible_states}")

    state_index = sum([val * (2**i) for i, val in enumerate(possible_states)])

    return state_index

def state_to_index(snake):
    """Returns a unique index for the state representation."""
    danger = _compute_danger(snake)
    red_apple = _compute_red_apple(snake)
    green_apple = _compute_green_apple(snake)

    logging.debug(f"State: {danger}, {red_apple}, {green_apple}")

    return danger * (4 * 7) + red_apple * 7 + green_apple

def print_Q_table_entry(Q_table, index):
    danger, red, green = index_to_state(index)

    state_label = f"{danger:<6} | {red:<7} | {green:<12}"
    row = " | ".join(f"{Q_table[index, j]:.2f}" for j in range(n_actions))
    logging.info(f"{state_label}: {row}")

def print_Q_table(Q_table):
    """Prints the Q-table in a readable format without affecting performance."""

    print("\nQ-table:")
    for state in range(NSTATES):
        print_Q_table_entry(Q_table, state)

def update_Q_table(Q_table, state, action, res, scenari, snake, alpha=0.1, gamma=0.9):
    """Updates the Q-table using the Q-learning algorithm."""
    reward = -1
    if res == False and scenari != "red":
        reward = -500
    else:
        if scenari == "red":
            reward = -80
        elif scenari == "green":
            reward = 80

    if res == False:
        return alpha * (reward - Q_table[state][action])
    else:
        next_state = state_to_index(snake)
        return alpha * (reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action])



NSTATES = 224  # 8 (Danger) * 4 (Red Apple) * 7 (Green Apple)
n_actions = 3  # Left, Right, Forward

Q_table = np.zeros((NSTATES, n_actions))


# Encore bcp de comportements randoms
# Le serpent devrait manger la pomme car il y a une pomme à côté et pas de mur mais il ne le fait pas
# Problème quand mur en face, pomme à droite mais mauvaise idée de manger la pomme car après serpent coincé
# Dans ce cas, il faudrait choisir le mur le plus éloigné pour prioriser la survie car il ne peut pas savoir qu'il va se retrouver coindé à priori

# Apres corrections des bugs on constate que manger une pomme verte n'est pas assez rewardé
# Pas assez de punitions pour rouge

def index_to_state(index):
    DANGER_LABELS = ["Safe", "Left", "Right", "Left+Right", "Center", "Left+Center", "Right+Center", "All"]
    RED_APPLE_LABELS = ["No Red", "Left", "Right", "Center"]
    GREEN_APPLE_LABELS = ["No Green", "Left", "Right", "Left+Right", "Center", "Left+Center", "Right+Center"]

    danger = index // (4 * 7)
    red_apple = (index % (4 * 7)) // 7
    green_apple = (index % 7)

    danger_label = DANGER_LABELS[danger]
    red_label = RED_APPLE_LABELS[red_apple]
    green_label = GREEN_APPLE_LABELS[green_apple]

    return danger_label, red_label, green_label

def is_state_possible(index):
    danger, red, green = index_to_state(index)

    danger_left = "Left" in danger or danger == "All"
    red_left = red == "Left"
    green_left = "Left" in green

    danger_right = "Right" in danger or danger == "All"
    red_right = red == "Right"
    green_right = "Right" in green

    danger_center = "Center" in danger or danger == "All"
    red_center = red == "Center"
    green_center = "Center" in green

    # Rule 1: "Danger Left" should not coexist with "Red Apple Left" or "Green Apple Left"
    if (danger_left and (red_left or green_left)):
        return False

    # Rule 2: "Danger Right" should not coexist with "Red Apple Right" or "Green Apple Right"
    if (danger_right and (red_right or green_right)):
        return False

    # Rule 3: "Danger Center" should not coexist with "Red Apple Center" or "Green Apple Center"
    if (danger_center and (red_center or green_center)):
        return False

    # Rule 4: "Red Apple Left" should not coexist with "Green Apple Left"
    if red_left and green_left:
        return False

    # Rule 5: "Red Apple Right" should not coexist with "Green Apple Right"
    if red_right and green_right:
        return False

    # Rule 6: "Red Apple Center" should not coexist with "Green Apple Center"
    if red_center and green_center:
        return False

    return True

def print_learning_progress(q_table, verbose = "minimal"):
    visited_states = 0
    taken_actions = 0
    state_count = 0
    for state in range(NSTATES):
        if is_state_possible(state):
            state_count += 1
            taken_actions += np.count_nonzero(q_table[state])
            if np.any(q_table[state]):
                visited_states += 1

            if verbose == "full":
                print_Q_table_entry(q_table, state)
            if verbose == "medium" and np.any(q_table[state] == 0):
                print_Q_table_entry(q_table, state)


    logging.info(f"Learning progress (state): {visited_states}/{state_count} ({(visited_states/state_count * 100):.2f} %)")
    logging.info(f"Learning progress (actions): {taken_actions}/{state_count * 3} ({(taken_actions/(state_count * 3) * 100):.2f} %)")
