import numpy as np
import random
from snake import Snake, direction_after_turn, DIRECTIONS

# Paramètres
gamma = 0.9   # Facteur de discount
alpha = 0.1   # Taux d'apprentissage
epsilon = 1.0  # Probabilité d'exploration (commence élevée, diminue ensuite)
epsilon_decay = 0.99  # Réduction d'epsilon après chaque épisode
num_episodes = 10000 # Nombre d'épisodes d'entraînement

n_actions = 3  # 3 actions possibles

# Here s = (danger_left, danger_right, danger_center)
# danger = 1 if wall or body immediate and 0 otherwise
# Total state = 3^2 = 9

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

NSTATES = 8
Q_table = np.zeros((NSTATES, n_actions))

for episode in range(num_episodes):
    print("Episode", episode, "================")
    snake = Snake()
    done = False

    while not done:
        state = state_to_index(snake)

        # Choix de l'action (epsilon-greedy)
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, n_actions - 1)  # Exploration
        else:
            action = np.argmax(Q_table[state])  # Exploitation

        # Exécuter l'action
        if action == 0:
            snake.turn("left")
        elif action == 1:
            snake.turn("right")

        res, scenari = snake.move()

        reward = -2
        if res == False:
            reward = -500
            done = True

        if done:
            Q_table[state][action] = Q_table[state][action] + alpha * (reward - Q_table[state][action])
            print("Score: ", snake.get_score())
        else:
            next_state = state_to_index(snake)
            Q_table[state, action] += alpha * (reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action])

    epsilon *= epsilon_decay

print(Q_table)


