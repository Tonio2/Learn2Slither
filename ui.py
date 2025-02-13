import pygame
import random
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
                    return "player"
                elif event.key == pygame.K_2:
                    return "ai"

def ai_random_move():
    return random.choice(["left", "right", None])


def main():
    mode = show_menu()
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
                }[event.key]
                snake.set_dir(direction)

        if mode == "ai":
            direction = ai_random_move()
            if direction is not None:
                snake.turn(direction)

        if not snake.move():
            print("Game Over")
            running = False  # Game over on collision

        clock.tick(3)

    pygame.quit()

if __name__ == "__main__":
    main()
