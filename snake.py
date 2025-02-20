import json
import random
from logger import logger as logging

BOARD_SIZE = 10

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Precomputed turn mappings (tuples are faster than dicts)
TURN_LEFT = [LEFT, UP, RIGHT, DOWN]
TURN_RIGHT = [RIGHT, DOWN, LEFT, UP]

def direction_after_turn(dir, turn):
    index = TURN_LEFT[dir] if turn == "left" else TURN_RIGHT[dir]
    return index

# First coordinate is the row, second is the column
class Snake:
    def __init__(self, board_size=BOARD_SIZE, initial_length=3, state=None, console=False):
        self.board_size = board_size
        self.history = []
        self.console = console

        if state:
            self._load_state(state)
            self.update_free_positions()
        else:
            self.free_positions = set(
                (x, y) for x in range(self.board_size) for y in range(self.board_size)
            )
            self.init_snake_pos(initial_length)
            self.green_apple_positions = set()
            self.red_apple_positions = set()
            self.free_positions -= set(self.positions)
            self._place_apples(2, "green")
            self._place_apples(1, "red")

        self._save_state()
        if console:
            self.log_console()


    def update_free_positions(self):
        self.free_positions = set(
            (x, y) for x in range(self.board_size) for y in range(self.board_size)
        )
        self.free_positions -= set(self.positions)
        self.free_positions -= self.green_apple_positions
        self.free_positions -= self.red_apple_positions

    def init_snake_pos(self, initial_length=3):
        pos_ok = False
        while not pos_ok:
            pos = self._get_free_random_position()
            self.dir = random.choice([UP, RIGHT, DOWN, LEFT])
            self.positions = [(pos[0] - i * DIRECTIONS[self.dir][0], pos[1] - i * DIRECTIONS[self.dir][1]) for i in range(initial_length)]
            pos_ok = all(self.is_legal(p) for p in self.positions)
            next_pos = self.next_pos(self.positions[0], self.dir)
            pos_ok = pos_ok and self.is_legal(next_pos)

    def _load_state(self, state):
        self.positions = [(p[0], p[1]) for p in state["positions"]]
        self.dir = state["dir"]
        self.green_apple_positions = set((pos[0], pos[1]) for pos in state["green_apples"])
        self.red_apple_positions = set((pos[0], pos[1]) for pos in state["red_apples"])

    def _save_state(self):
        state = {
            "positions": self.positions[:],
            "dir": self.dir,
            "green_apples": list(self.green_apple_positions),
            "red_apples": list(self.red_apple_positions),
        }
        self.history.append(state)

    def log_console(self):
        readable_dir = ["UP", "RIGHT", "DOWN", "LEFT"]
        print(readable_dir[self.dir])
        print()
        for row in range(-1, self.board_size + 1):
            for col in range(-1, self.board_size + 1):
                if row == self.positions[0][0] or col == self.positions[0][1]:
                    if row == -1 or row == self.board_size or col == -1 or col == self.board_size:
                        print("W", end="")
                    elif (row, col) in self.positions:
                        print("S", end="")
                    elif (row, col) in self.green_apple_positions:
                        print("G", end="")
                    elif (row, col) in self.red_apple_positions:
                        print("R", end="")
                    else:
                        print("0", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def _get_free_random_position(self):
        if not self.free_positions:
            return None
        return random.choice(list(self.free_positions))

    def _place_apples(self, count, color):
        placed = False
        for _ in range(count):
            pos = self._get_free_random_position()
            if pos:
                if color == "green":
                    self.green_apple_positions.add(pos)
                else:
                    self.red_apple_positions.add(pos)

                self.free_positions.remove(pos)
                placed = True
        return placed


    def set_dir(self, command):
        if command not in [UP, RIGHT, DOWN, LEFT]:
            raise ValueError(f"Direction invalide : {command}")
        if DIRECTIONS[command] != (-DIRECTIONS[self.dir][0], -DIRECTIONS[self.dir][1]):
            self.dir = command

    def turn(self, dir):
        self.set_dir(direction_after_turn(self.dir, dir))

    def _pop_tail(self):
        tail = self.positions.pop()
        self.free_positions.add(tail)

    def _insert_head(self, head):
        self.positions.insert(0, head)
        self.free_positions.discard(head)

    def next_pos(self, pos, dir):
        if dir not in [UP, RIGHT, DOWN, LEFT]:
            raise ValueError(f"Direction invalide : {dir}")
        return (pos[0] + DIRECTIONS[dir][0], pos[1] + DIRECTIONS[dir][1])

    def is_legal(self, pos):
        return pos[0] >= 0 and pos[0] < self.board_size and pos[1] >= 0 and pos[1] < self.board_size

    def tile_type(self, pos):
        if not self.is_legal(pos):
            return "wall"
        if pos in self.positions:
            return "snake"
        if pos in self.green_apple_positions:
            return "green"
        if pos in self.red_apple_positions:
            return "red"
        return "empty"


    def _make_move(self):
        head = self.positions[0]
        new_head = self.next_pos(head, self.dir)

        scenari = self.tile_type(new_head)

        if scenari == "wall":
            return False, scenari
        if scenari == "snake":
            if new_head == self.positions[-1]:
                scenari = "empty"
            else:
                return False, scenari
        if scenari == "red" and len(self.positions) == 1:
            return False, scenari

        # Update snake
        self._insert_head(new_head)
        if scenari != "green":
            self._pop_tail()
        if scenari == "red":
            self._pop_tail()

        # Update apples
        if scenari in ["green", "red"]:
            if scenari == "green":
                self.green_apple_positions.remove(new_head)
            else:
                self.red_apple_positions.remove(new_head)
            if not self._place_apples(1, scenari):
                return False, scenari

        return True, scenari

    def move(self):
        res, scenari = self._make_move()
        logging.debug(f'Move: {self.dir} Result: {res} Scenari: {scenari}')
        self._save_state()
        if self.console:
            self.log_console()
        return res, scenari

    def get_positions(self):
        return self.positions

    def get_head_position(self):
        return self.positions[0]

    def get_score(self):
        return len(self.positions) - 3

    def save_game(self, filename="game_history.json"):
        with open(filename, "w") as f:
            json.dump(self.history, f)
