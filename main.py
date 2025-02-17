import json
import os
import numpy as np
from snake import Snake
from snakeUI import UI
from v1.strategy import print_Q_table_entry

ui = UI()
replay = True

def get_available_models():
    """Detect available AI models by looking for subdirectories with Q-table files."""
    models = []
    for folder in os.listdir():
        if os.path.isdir(folder) and os.path.exists(os.path.join(folder, "Q_table.npy")):
            models.append(folder)
    return models

def main():
    show_menu = True

    while True:

        if show_menu:
            models = get_available_models()
            mode, selected_model = ui.show_menu(models)

        if mode == "ai":
            model_path = os.path.join(selected_model, "Q_table.npy")
            q_table = np.load(model_path)
            from importlib import import_module
            strategy_module = import_module(f"{selected_model}.strategy")
            state_to_index = strategy_module.state_to_index

        if replay and mode == "ai":
            with open("game_history.json") as f:
                history = json.load(f)
            h_idx = 0
            snake = Snake(state=history[h_idx])
        else:
            snake = Snake()
        running = True
        direction = None



        while running:
            ui.render(snake)

            if mode == "ai":
                print("==================")
                state = state_to_index(snake)
                print_Q_table_entry(q_table, state)

            events = ui.get_events()
            if "quit" in events:
                ui.quit()
                running = False
            if "direction" in events and mode == "player":
                direction = events["direction"]
                if (direction != None):
                    snake.set_dir(direction)
            if ("speed" in events and mode == "ai"):
                ui.set_speed(events["speed"])
            if "step" in events and replay:
                h_idx += min(0, events["step"])


            if mode == "ai" and not replay:
                action = np.argmax(q_table[state])
                direction = ["left", "right", None][action]
                if direction:
                    snake.turn(direction)



            if replay and mode == "ai":
                h_idx += 1
                if h_idx < len(history):
                    snake = Snake(state=history[h_idx])
                else:
                    print("Game Over")
                    running = False
            else:
                if not snake.move()[0]:
                    print("Game Over")
                    running = False  # Game over on collision
                    snake.save_game()

        option = ui.game_over_screen(snake)
        if option == "Play Again":
            show_menu = False
        if option == "Main Menu":
            show_menu = True
        elif option == "Quit":
            ui.quit()
            return

if __name__ == "__main__":
    main()
