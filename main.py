import pygame
import random
import os
import numpy as np
from snake import Snake, UP, DOWN, LEFT, RIGHT

# Constants
SCREEN_SIZE = 400
CELL_SIZE = SCREEN_SIZE // 10
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Snake Game")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def get_available_models():
    """Detect available AI models by looking for subdirectories with Q-table files."""
    models = []
    for folder in os.listdir():
        if os.path.isdir(folder) and os.path.exists(os.path.join(folder, "Q_table.npy")):
            models.append(folder)
    return models

def draw_snake(snake):
    for pos in snake.get_positions():
        pygame.draw.rect(screen, WHITE, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_apples(snake):
    for apple in snake.green_apple_positions:
        pygame.draw.rect(screen, GREEN, (apple[1] * CELL_SIZE, apple[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for apple in snake.red_apple_positions:
        pygame.draw.rect(screen, RED, (apple[1] * CELL_SIZE, apple[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def show_menu():
    screen.fill(BLACK)
    title = font.render("Select Mode", True, WHITE)
    player_option = font.render("1. Player", True, WHITE)
    ai_option = font.render("2. AI", True, WHITE)

    screen.blit(title, (SCREEN_SIZE // 3, SCREEN_SIZE // 4))
    screen.blit(player_option, (SCREEN_SIZE // 3, SCREEN_SIZE // 2))
    screen.blit(ai_option, (SCREEN_SIZE // 3, SCREEN_SIZE // 2 + 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "player", None
                elif event.key == pygame.K_2:
                    return "ai", select_ai_model()

def select_ai_model():
    models = get_available_models()
    if not models:
        print("No AI models found! Defaulting to v0.")
        return "v0"

    selected = 0
    while True:
        screen.fill(BLACK)
        title = font.render("Select AI Model", True, WHITE)
        screen.blit(title, (SCREEN_SIZE // 4, SCREEN_SIZE // 6))

        for i, model in enumerate(models):
            color = GREEN if i == selected else WHITE
            text = font.render(f"> {model} " if i == selected else model, True, color)
            screen.blit(text, (SCREEN_SIZE // 4, SCREEN_SIZE // 3 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected > 0:
                    selected -= 1
                elif event.key == pygame.K_DOWN and selected < len(models) - 1:
                    selected += 1
                elif event.key == pygame.K_RETURN:
                    return models[selected]

def main():
    mode, selected_model = show_menu()

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
        screen.fill(BLACK)
        draw_apples(snake)
        draw_snake(snake)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if mode == "player" and event.type == pygame.KEYDOWN:
                direction = {
                    pygame.K_UP: UP,
                    pygame.K_DOWN: DOWN,
                    pygame.K_LEFT: LEFT,
                    pygame.K_RIGHT: RIGHT,
                }.get(event.key, direction)
                if direction:
                    snake.set_dir(direction)

        if mode == "ai":
            state = state_to_index(snake)
            action = np.argmax(q_table[state])
            direction = None
            if action == 0:
                direction = "left"
            elif action == 1:
                direction = "right"
            if direction:
                snake.turn(direction)

        if not snake.move()[0]:
            print("Game Over")
            running = False  # Game over on collision

        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()
