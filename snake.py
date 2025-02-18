import json
import random

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
    def __init__(self, board_size=BOARD_SIZE, initial_length=3, state=None):
        self.board_size = board_size

        self.free_positions = set(
            (x, y) for x in range(self.board_size) for y in range(self.board_size)
        )

        pos_ok = False
        while not pos_ok:
            pos = self._get_free_random_position()
            self.dir = random.choice([UP, RIGHT, DOWN, LEFT])
            self.positions = [(pos[0] - i * DIRECTIONS[self.dir][0], pos[1] - i * DIRECTIONS[self.dir][1]) for i in range(initial_length)]
            pos_ok = all(self.is_legal(p) for p in self.positions)
            next_pos = self.next_pos(self.positions[0], self.dir)
            pos_ok = pos_ok and self.is_legal(next_pos)

        print(self.positions)

        self.free_positions -= set(self.positions)

        self.green_apple_positions = set()
        self.red_apple_positions = set()

        self.history = []

        self._place_apples(2, "green")
        self._place_apples(1, "red")
        self._save_state()

        if state:
            self._load_state(state)

    def _load_state(self, state):
        self.positions = state["positions"]
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


    def _get_free_random_position(self):
        if not self.free_positions:
            return None
        return random.choice(list(self.free_positions))

    def _place_apples(self, count, color):
        for _ in range(count):
            pos = self._get_free_random_position()
            if pos:
                if color == "green":
                    self.green_apple_positions.add(pos)
                else:
                    self.red_apple_positions.add(pos)

                self.free_positions.remove(pos)

    def set_dir(self, command):
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
        return (pos[0] + DIRECTIONS[dir][0], pos[1] + DIRECTIONS[dir][1])

    def is_legal(self, pos):
        return pos[0] >= 0 and pos[0] < self.board_size and pos[1] >= 0 and pos[1] < self.board_size

    def _make_move(self):
        head_x, head_y = self.positions[0]
        new_head = self.next_pos((head_x, head_y), self.dir)
        scenari = "default"

        # print("New head:", new_head)

        if (
            new_head in self.positions
            or new_head[0] < 0 or new_head[0] >= self.board_size
            or new_head[1] < 0 or new_head[1] >= self.board_size
        ):
            # print("Eats its body: ", new_head in self.positions)
            # print("Hits wall: ", new_head[0] < 0 or new_head[0] >= self.board_size or new_head[1] < 0 or new_head[1] >= self.board_size)
            return False, scenari # Collision detected

        if new_head in self.green_apple_positions:
            scenari = "green"
        elif new_head in self.red_apple_positions:
            scenari = "red"

        # Update snake
        self._insert_head(new_head)
        if scenari == "default":
            self._pop_tail()
        elif scenari == "red":
            if len(self.positions) > 2:
                self._pop_tail()
                self._pop_tail()
            else:
                print("Eats red apple but not enough length")
                return False, scenari

        # Update apples
        if scenari == "green":
            self.green_apple_positions.remove(new_head)
            self._place_apples(1, "green")
        elif scenari == "red":
            self.red_apple_positions.remove(new_head)
            self._place_apples(1, "red")

        return True, scenari

    def move(self):
        res, scenari = self._make_move()
        # print("Move:", self.dir, "Result:", res, "Scenari:", scenari)
        self._save_state()
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
