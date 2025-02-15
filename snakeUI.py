import pygame
from snake import Snake

# Constants
SCREEN_SIZE = 400
CELL_SIZE = SCREEN_SIZE // 10
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class UI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Snake Game")
        font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def _draw_apples(self, snake):
        for apple in snake.green_apple_positions:
            pygame.draw.rect(self.screen, GREEN, (apple[1] * CELL_SIZE, apple[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for apple in snake.red_apple_positions:
            pygame.draw.rect(self.screen, RED, (apple[1] * CELL_SIZE, apple[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def _draw_snake(self, snake):
        for pos in snake.get_positions():
            pygame.draw.rect(self.screen, WHITE, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def render(self, snake):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.clock.tick(100)

        self.screen.fill(BLACK)
        self._draw_apples(snake)
        self._draw_snake(snake)

        pygame.display.flip()
