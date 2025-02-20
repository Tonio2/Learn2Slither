import argparse
import json
import os
import random
import numpy as np
from importlib import import_module
from snakeUI import UI
from snake import Snake
import shutil
from logger import logger as logging


def load(model_name, train=False):
    strategy_module = import_module(f"{model_name}.strategy")
    state_to_index = strategy_module.state_to_index
    update_q_table = strategy_module.update_Q_table
    print_Q_table_entry = strategy_module.print_Q_table_entry
    print_learning_progress = strategy_module.print_learning_progress

    if train:
        q_table = strategy_module.Q_table
    else:
        model_path = os.path.join(model_name, "Q_table.npy")
        q_table = np.load(model_path)
    return q_table, state_to_index, update_q_table, print_Q_table_entry, print_learning_progress

def play():
    ui = UI()
    playing = True

    while playing:
        snake = Snake()
        running = True

        while running:
            ui.render(snake)

            input = ui.get_player_input()

            if input == "quit":
                ui.quit()
                running = False
            elif input is not None:
                snake.set_dir(input)

            res, _ = snake.move()
            if not res:
                snake.save_game()
                running = False

        option = ui.game_over_screen(snake.get_score())
        if option == "Quit":
            playing = False

    ui.quit()


def train(ui_flag, q_table, state_to_index, update_q_table, model_name, print_learning_progress):
    gamma = 0.9
    alpha = 0.1
    epsilon = 1.0
    epsilon_decay = 0.99
    num_episodes = 2000

    if ui_flag:
        ui = UI()

    for episode in range(num_episodes):
        snake = Snake()
        nmoves = 0
        result = True

        while result and nmoves < 1000:
            if ui_flag:
                ui.render(snake)
                input_type, _ = ui.get_spectator_input()
                if input_type == "quit":
                    break

            state = state_to_index(snake)
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 2)
            else:
                action = np.argmax(q_table[state])

            if action == 0:
                snake.turn("left")
            elif action == 1:
                snake.turn("right")

            result, scenari = snake.move()
            q_table[state, action] += update_q_table(q_table, state, action, result, scenari, snake, alpha, gamma)

            nmoves += 1

        score = snake.get_score()
        logging.info(f"Episode: {episode} Score: {score} Epsilon: {epsilon:.4f}")
        epsilon = max(0.1, epsilon * epsilon_decay)

        if ui_flag and input_type == "quit":
            break

    print_learning_progress(q_table, verbose = "medium")

    if ui_flag:
        ui.quit()

def test(ui_flag, q_table, state_to_index, ngames, save, print_Q_table_entry):
    scores = []

    if ui_flag:
        ui = UI()

    if save:
        if os.path.exists("replays"):
            shutil.rmtree("replays")
        os.makedirs("replays", exist_ok=True)

    for episode in range(ngames):
        snake = Snake()
        nmoves = 0
        result = True

        while result and nmoves < 1000:
            state = state_to_index(snake)
            # print_Q_table_entry(q_table, state)
            if ui_flag:
                ui.render(snake)
                input_type, _ = ui.get_spectator_input()

                if input_type == "quit":
                    break


            action = np.argmax(q_table[state])

            if action == 0:
                snake.turn("left")
            elif action == 1:
                snake.turn("right")

            result, _ = snake.move()

            nmoves += 1

        logging.info(f'Episode: {episode} Score: {snake.get_score()}')
        scores.append(snake.get_score())

        if save:
            snake.save_game(f"replays/game_{episode}.json")

        if ui_flag and input_type == "quit":
            break

    logging.info(f'Average score: , {sum(scores) / ngames}')

    if ui_flag:
        ui.quit()

def replay(ui_flag, filename, q_table, state_to_index, print_Q_table_entry):
    with open(filename) as f:
        history = json.load(f)

    if ui_flag:
        ui = UI()

    h_idx = 0
    snake = Snake(state=history[h_idx])
    running = True

    while running:
        index = state_to_index(snake)
        print_Q_table_entry(q_table, index)
        if ui_flag:
            ui.render(snake)
            input_type, value = ui.get_spectator_input()

            if input_type == "quit":
                break
            if input_type == "step":
                h_idx = max(0, h_idx + value)

        h_idx += 1
        if h_idx < len(history):
            snake = Snake(state=history[h_idx])
        else:
            logging.info("Game Over")
            running = False

    if ui_flag:
        ui.quit()

DEFAULT = "v2"
if __name__ == "__main__":
    parser = argparse.ArgumentParser("AI learning to play snake through Q-learning")
    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")

    play_parser = subparsers.add_parser("play", help="Jouer au jeu")

    replay_parser = subparsers.add_parser("replay", help="Rejouer une partie")
    replay_parser.add_argument("filename", help="Fichier de replay")
    replay_parser.add_argument("--model", default=DEFAULT, help="Modèle d'IA")
    replay_parser.add_argument("--no-ui", action="store_true", help="Mode console")

    train_parser = subparsers.add_parser("train", help="Entraîner un modèle d'IA")
    train_parser.add_argument("--model", default=DEFAULT, help="Nom du modèle")
    train_parser.add_argument("--no-ui", action="store_true", help="Mode console")

    test_parser = subparsers.add_parser("test", help="Tester un modèle d'IA")
    test_parser.add_argument("--model", default=DEFAULT, help="Nom du modèle")
    test_parser.add_argument("--games", default=1, type=int, help="Nombre de parties à jouer")
    test_parser.add_argument("--no-ui", action="store_true", help="Mode console")
    test_parser.add_argument("--save", action="store_true", help="Sauvegarder les parties")

    visualize_parser = subparsers.add_parser("visualize", help="Visualiser un modèle d'IA")
    visualize_parser.add_argument("--model", default=DEFAULT, help="Nom du modèle")

    args = parser.parse_args()

    MODE = args.command

    if MODE == "play":
        play()
    else:
        q_table, state_to_index, update_q_table, print_Q_table_entry, print_learning_progress = load(args.model, MODE == "train")
        if MODE == "replay":
            replay(not args.no_ui, args.filename, q_table, state_to_index, print_Q_table_entry)
        if MODE == "train":
            train(not args.no_ui, q_table, state_to_index, update_q_table, args.model, print_learning_progress)
        if MODE == "test":
            test(not args.no_ui, q_table, state_to_index, args.games, args.save, print_Q_table_entry)
        if MODE == "visualize":
            print_learning_progress(q_table, verbose="medium")

