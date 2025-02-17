import pygame
from snake import UP, DOWN, LEFT, RIGHT

QUIT = 5

# Constants
SCREEN_SIZE = 400
UI_HEIGHT = 50
TOTAL_HEIGHT = SCREEN_SIZE + UI_HEIGHT


CELL_SIZE = SCREEN_SIZE // 10
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)  # Background for UI bar

class UI:
    def __init__(self, turn_based = False):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, TOTAL_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.max_fps = 5
        self.turn_based = turn_based

    def _draw_apples(self, snake):
        for apple in snake.green_apple_positions:
            pygame.draw.rect(self.screen, GREEN, (apple[1] * CELL_SIZE, apple[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for apple in snake.red_apple_positions:
            pygame.draw.rect(self.screen, RED, (apple[1] * CELL_SIZE, apple[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def _draw_snake(self, snake):
        for pos in snake.get_positions():
            pygame.draw.rect(self.screen, WHITE, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def _draw_ui(self, score):
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_SIZE, SCREEN_SIZE, UI_HEIGHT))  # UI bar background

        score_text = self.font.render(f"Score: {score}", True, WHITE)
        speed_text = self.font.render(f"Speed: {'Turn-Based' if self.turn_based else f'{self.max_fps} FPS'}", True, WHITE)

        self.screen.blit(score_text, (10, SCREEN_SIZE + 5))
        self.screen.blit(speed_text, (150, SCREEN_SIZE + 5))

    def render(self, snake):
        self.screen.fill(BLACK)
        self._draw_apples(snake)
        self._draw_snake(snake)
        self._draw_ui(snake.get_score())  # Draw UI elements
        pygame.display.flip()
        self.clock.tick(1000 if self.turn_based else self.max_fps)

    def get_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return UP
                elif event.key == pygame.K_DOWN:
                    return DOWN
                elif event.key == pygame.K_LEFT:
                    return LEFT
                elif event.key == pygame.K_RIGHT:
                    return RIGHT

        return None

    def get_spectator_input(self):
        if self.turn_based:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "quit", 0
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            return None, 0
                        if event.key == pygame.K_LEFT:
                            return "step", -2
                        if event.key == pygame.K_SPACE:
                            self.turn_based = not self.turn_based
                            return None, 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.turn_based = not self.turn_based
                if event.key == pygame.K_RIGHT:
                    self.max_fps += 1
                if event.key == pygame.K_LEFT:
                    self.max_fps = max(1, self.max_fps - 1)
        return None, 0

    def quit(self):
        pygame.quit()

    def set_speed(self, speed):
        if speed == "slower":
            self.max_fps = max(1, self.max_fps - 1)
        elif speed == "faster":
            self.max_fps += 1
        elif speed == "pause":
            self.turn_based = not self.turn_based

    def select_ai_model(self, models):
        if not models:
            print("No AI models found! Defaulting to v0.")
            return "v0"

        selected = 0
        while True:
            self.screen.fill(BLACK)
            title = self.font.render("Select AI Model", True, WHITE)
            self.screen.blit(title, (SCREEN_SIZE // 4, SCREEN_SIZE // 6))

            for i, model in enumerate(models):
                color = GREEN if i == selected else WHITE
                text = self.font.render(f"> {model} " if i == selected else model, True, color)
                self.screen.blit(text, (SCREEN_SIZE // 4, SCREEN_SIZE // 3 + i * 40))

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

    def show_menu(self, models):
        self.screen.fill(BLACK)
        title = self.font.render("Select Mode", True, WHITE)
        player_option = self.font.render("1. Player", True, WHITE)
        ai_option = self.font.render("2. AI", True, WHITE)

        self.screen.blit(title, (SCREEN_SIZE // 3, SCREEN_SIZE // 4))
        self.screen.blit(player_option, (SCREEN_SIZE // 3, SCREEN_SIZE // 2))
        self.screen.blit(ai_option, (SCREEN_SIZE // 3, SCREEN_SIZE // 2 + 40))
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
                        return "ai", self.select_ai_model(models)

    def game_over_screen(self, score):

        selected = 0
        while True:
            self.screen.fill(BLACK)
            title = self.font.render("GAME OVER", True, WHITE)
            self.screen.blit(title, (SCREEN_SIZE // 4, SCREEN_SIZE // 6))

            score_text = self.font.render(f"Score: {score}", True, WHITE)
            self.screen.blit(score_text, (SCREEN_SIZE // 4, SCREEN_SIZE // 6 + 40))

            options = ["Play Again", "Quit"]
            for i, option in enumerate(options):
                color = GREEN if i == selected else WHITE
                text = self.font.render(f"> {option} " if i == selected else option, True, color)
                self.screen.blit(text, (SCREEN_SIZE // 4, SCREEN_SIZE // 6 + 120 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and selected > 0:
                        selected -= 1
                    elif event.key == pygame.K_DOWN and selected < len(options) - 1:
                        selected += 1
                    elif event.key == pygame.K_RETURN:
                        return options[selected]
