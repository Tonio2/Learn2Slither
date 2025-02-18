import pygame
import pygame.gfxdraw
from snake import UP, DOWN, LEFT, RIGHT

# Constants
SCREEN_SIZE = 400
UI_HEIGHT = 50
TOTAL_HEIGHT = SCREEN_SIZE + UI_HEIGHT
CELL_SIZE = SCREEN_SIZE // 10

# Colors
WHITE = (255, 255, 255)
SNAKE_GREEN = (0, 255, 0)       # Bright retro-green for snake
BLACK = (0, 0, 0)
DARK_BG = (20, 20, 40)          # Dark bluish background
NAVBAR_BG = (35,48,83)        # Slightly lighter dark background for the navbar
GRID_DARK = (46,59,93)        # Dark cell color
GRID_LIGHT = (57,69,107)      # Light cell color for checker pattern
FONT = (109,124,174)

class UI:
    def __init__(self, turn_based=False):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, TOTAL_HEIGHT))
        pygame.display.set_caption("🐍 Snake Game")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.max_fps = 5
        self.turn_based = turn_based

    def _draw_grid_background(self):
        """
        Draws a checkerboard-style grid in the game area
        (below the navbar).
        """
        # The game board starts at y = UI_HEIGHT
        for row in range(10):
            for col in range(10):
                # Each cell is CELL_SIZE x CELL_SIZE
                rect = pygame.Rect(
                    col * CELL_SIZE,
                    row * CELL_SIZE + UI_HEIGHT,  # offset by navbar height
                    CELL_SIZE,
                    CELL_SIZE
                )
                if (row + col) % 2 == 0:
                    color = GRID_DARK
                else:
                    color = GRID_LIGHT
                pygame.draw.rect(self.screen, color, rect)

    def _draw_navbar(self, score):
        """
        Draws the top navbar with Score and Speed.
        """
        navbar_rect = pygame.Rect(0, 0, SCREEN_SIZE, UI_HEIGHT)
        pygame.draw.rect(self.screen, NAVBAR_BG, navbar_rect)

        score_text = self.font.render(f"SCORE: {score}", True, FONT)
        if self.turn_based:
            speed_str = "0 FPS"
        else:
            speed_str = f"{self.max_fps} FPS"
        speed_text = self.font.render(f"SPEED: {speed_str}", True, FONT)

        # Position them inside the navbar
        self.screen.blit(score_text, (15, 14))
        self.screen.blit(speed_text, (220, 14))

    def _draw_apples(self, snake):
        if not hasattr(self, 'green_apple_img'):
            self.green_apple_img = pygame.image.load("img/green_apple.png")
            self.green_apple_img = pygame.transform.scale(self.green_apple_img, (CELL_SIZE, CELL_SIZE))

        if not hasattr(self, 'red_apple_img'):
            self.red_apple_img = pygame.image.load("img/red_apple.png")
            self.red_apple_img = pygame.transform.scale(self.red_apple_img, (CELL_SIZE, CELL_SIZE))

        for apple in snake.green_apple_positions:
            x = apple[1] * CELL_SIZE
            y = apple[0] * CELL_SIZE + UI_HEIGHT
            self.screen.blit(self.green_apple_img, (x, y))

        for apple in snake.red_apple_positions:
            x = apple[1] * CELL_SIZE
            y = apple[0] * CELL_SIZE + UI_HEIGHT
            self.screen.blit(self.red_apple_img, (x, y))


    def _draw_snake(self, snake):
        """
        Draws the snake. The head has small eyes.
        """
        positions = snake.get_positions()
        if not positions:
            return

        # Draw head separately so we can give it eyes
        head = positions[0]
        head_rect = pygame.Rect(
            head[1] * CELL_SIZE,
            head[0] * CELL_SIZE + UI_HEIGHT,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(self.screen, SNAKE_GREEN, head_rect)

        # Determine snake direction for eye placement
        direction = snake.dir
        eye_radius = 2
        head_x = head_rect.x
        head_y = head_rect.y

        # Default eye positions (if facing right)
        left_eye_center = (head_x + CELL_SIZE // 4, head_y + CELL_SIZE // 4)
        right_eye_center = (head_x + 3 * CELL_SIZE // 4, head_y + CELL_SIZE // 4)

        if direction == DOWN:
            left_eye_center  = (head_x + CELL_SIZE // 4, head_y + 3 * CELL_SIZE // 4)
            right_eye_center = (head_x + 3 * CELL_SIZE // 4, head_y + 3 * CELL_SIZE // 4)
        elif direction == LEFT:
            left_eye_center  = (head_x + CELL_SIZE // 4, head_y + CELL_SIZE // 4)
            right_eye_center = (head_x + CELL_SIZE // 4, head_y + 3 * CELL_SIZE // 4)
        elif direction == RIGHT:
            left_eye_center  = (head_x + 3 * CELL_SIZE // 4, head_y + CELL_SIZE // 4)
            right_eye_center = (head_x + 3 * CELL_SIZE // 4, head_y + 3 * CELL_SIZE // 4)

        # Draw eyes (small black circles)
        pygame.gfxdraw.filled_circle(self.screen, left_eye_center[0], left_eye_center[1], eye_radius, BLACK)
        pygame.gfxdraw.filled_circle(self.screen, right_eye_center[0], right_eye_center[1], eye_radius, BLACK)

        # Draw the rest of the body
        for pos in positions[1:]:
            rect = pygame.Rect(
                pos[1] * CELL_SIZE,
                pos[0] * CELL_SIZE + UI_HEIGHT,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, SNAKE_GREEN, rect)

    def render(self, snake):
        # 1) Draw the top navbar
        self._draw_navbar(snake.get_score())

        # 2) Draw the checkerboard background for the game area
        self._draw_grid_background()

        # 3) Draw apples and snake
        self._draw_apples(snake)
        self._draw_snake(snake)

        pygame.display.flip()
        self.clock.tick(1000 if self.turn_based else self.max_fps)


    def get_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

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
                color = SNAKE_GREEN if i == selected else WHITE
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
                color = SNAKE_GREEN if i == selected else WHITE
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
