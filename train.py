import numpy as np
import random
from snake import Snake
from snakeUI import UI
from v1.strategy import state_to_index, Q_table, print_Q_table, update_Q_table


def choose_action(Q_table, state, epsilon):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, n_actions - 1)  # Exploration
    else:
        return np.argmax(Q_table[state])  # Exploitation

def execute_action(action, snake):
    if action == 0:
        snake.turn("left")
    elif action == 1:
        snake.turn("right")

    res, scenari = snake.move()
    return res, scenari

# Paramètres
gamma = 0.9   # Facteur de discount
alpha = 0.1   # Taux d'apprentissage
epsilon = 1.0  # Probabilité d'exploration (commence élevée, diminue ensuite)
epsilon_decay = 0.99  # Réduction d'epsilon après chaque épisode
num_episodes = 10000 # Nombre d'épisodes d'entraînement

n_actions = 3  # 3 actions possibles
mode = "no_ui" # "ui" or "no_ui"

if mode == "ui":
    ui = UI()

def game(Q_table, epsilon):
    snake = Snake()
    done = False

    while not done:
        if mode == "ui":
            ui.render(snake)
            events = ui.get_events()
            if "quit" in events:
                ui.quit()
                return Q_table

        state = state_to_index(snake)
        action = choose_action(Q_table, state, epsilon)
        result, scenari = execute_action(action, snake)
        Q_table[state, action] += update_Q_table(Q_table, state, action, result, scenari, snake, alpha, gamma)

        if not result:
            done = True
            print("Score: ", snake.get_score())

    return Q_table

for episode in range(num_episodes):
    print("Episode", episode, "================")

    Q_table = game(Q_table, epsilon)

    epsilon *= epsilon_decay

print_Q_table(Q_table)
np.save("Q_table.npy", Q_table)
