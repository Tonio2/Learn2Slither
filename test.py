from snakeUI import UI
from snake import Snake
from v1.strategy import state_to_index
import numpy as np

mode = "no_ui"
n_games = 1000
scores = []

def main():
    if mode == "ui":
        ui = UI()

    q_table = np.load("v1/Q_table.npy")

    for i in range(n_games):
        snake = Snake()
        done = False
        n_moves = 0

        while not done and n_moves < 2000:

            if mode == "ui":
                ui.render(snake)
                events = ui.get_events()
                if "quit" in events:
                    ui.quit()
                    return

            state = state_to_index(snake)
            action = np.argmax(q_table[state])
            direction = ["left", "right", None][action]
            if direction:
                snake.turn(direction)


            result, _ = snake.move()

            if not result:
                done = True

            n_moves += 1

        scores.append(snake.get_score())

    print("Average score:", sum(scores) / n_games)
    if mode == "ui":
        ui.quit()

if __name__ == "__main__":
    main()
