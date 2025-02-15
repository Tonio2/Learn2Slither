import os
import numpy as np
from snake import Snake
from snakeUI import UI
from v1.strategy import print_Q_table_entry

ui = UI()

def get_available_models():
    """Detect available AI models by looking for subdirectories with Q-table files."""
    models = []
    for folder in os.listdir():
        if os.path.isdir(folder) and os.path.exists(os.path.join(folder, "Q_table.npy")):
            models.append(folder)
    return models

def main():
    models = get_available_models()
    mode, selected_model = ui.show_menu(models)

    if mode == "ai":
        model_path = os.path.join(selected_model, "Q_table.npy")
        q_table = np.load(model_path)
        from importlib import import_module
        strategy_module = import_module(f"{selected_model}.strategy")
        state_to_index = strategy_module.state_to_index

    snake = Snake()
    running = True
    direction = None

    while running:
        ui.render(snake, snake.get_score())

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
        if "speed" in events:
            ui.set_speed(events["speed"])

        if mode == "ai":
            action = np.argmax(q_table[state])
            direction = ["left", "right", None][action]
            if direction:
                snake.turn(direction)

        if not snake.move()[0]:
            print("Game Over")
            running = False  # Game over on collision

    ui.quit()

if __name__ == "__main__":
    main()
