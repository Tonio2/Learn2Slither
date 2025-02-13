import random

BOARD_SIZE = 10

LEFT_CMD = -1
RIGHT_CMD = 1

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS = [UP,RIGHT,DOWN,LEFT]

class Snake:
    def __init__(self, board_size=BOARD_SIZE, initial_length=3):
        self.board_size = board_size
        self.positions = [(0, i) for i in range(initial_length)]
        self.dir_idx = 3

        self.free_positions = set(
            (x, y) for x in range(self.board_size) for y in range(self.board_size)
        )
        self.free_positions -= set(self.positions)

        self.green_apple_positions = set()
        self.red_apple_positions = set()

        self._place_apples(2, "green")
        self._place_apples(1, "red")



    def _get_free_random_position(self):
        if not self.free_positions:
            return None
        return random.choice(self.free_positions)

    def _place_apples(self, count, color):
        for _ in range(count):
            pos = self._get_free_random_position()
            if pos:
                if color == "green":
                    self.green_apple_positions.add(pos)
                else:
                    self.red_apple_positions.add(pos)

                self.free_positions.remove(pos)

    def change_direction(self, command):
        # command should be LEFT_CMD or RIGHT_CMD
        self.dir_idx = (self.dir_idx + command) % 4

    def _pop_tail(self):
        tail = self.positions.pop()
        self.free_positions.add(tail)

    def _insert_head(self, head):
        self.positions.insert(0, head)
        self.free_positions.remove(head)

    def move(self):
        head_x, head_y = self.positions[0]
        new_head = (head_x + DIRS[self.dir_idx][0], head_y + DIRS[self.dir_idx][1])
        scenari = "default"

        if (
            new_head in self.positions
            or new_head[0] < 0 or new_head[0] >= self.board_size
            or new_head[1] < 0 or new_head[1] >= self.board_size
        ):
            return False # Collision detected

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
                return False

        # Update apples
        if scenari == "green":
            self.green_apple_positions.remove(new_head)
            self._place_apples(1, "green")
        elif scenari == "red":
            self.red_apple_positions.remove(new_head)
            self._place_apples(1, "red")

        return True

    def get_positions(self):
        return self.positions

    def get_head_position(self):
        return self.positions[0]
