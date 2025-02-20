import pytest
from snake import Snake, direction_after_turn, UP, RIGHT, DOWN, LEFT
from unittest.mock import patch

def test_place_apples():
    snake = Snake(board_size=5)

    initial_free_positions = len(snake.free_positions)
    initial_green_count = len(snake.green_apple_positions)

    snake._place_apples(3, "green")

    # Vérifie qu'on a bien ajouté 3 pommes
    assert len(snake.green_apple_positions) == initial_green_count + 3

    # Vérifie qu'on a bien retiré 3 cases des positions libres
    assert len(snake.free_positions) == initial_free_positions - 3

def test_set_dir():
    snake = Snake()

    dirs = [UP, RIGHT, DOWN, LEFT]
    opposite_dirs = [DOWN, LEFT, UP, RIGHT]

    for i, dir in enumerate(dirs):
        initial_dir = snake.dir

        snake.set_dir(dir)

        if initial_dir == opposite_dirs[i]:
            assert snake.dir == initial_dir
        else:
            assert snake.dir == dir

def test_set_dir_invalid():
    snake = Snake()

    with pytest.raises(ValueError):
        snake.set_dir(99)

    with pytest.raises(ValueError):
        snake.set_dir(-1)

    with pytest.raises(ValueError):
        snake.set_dir("up")

def test_direction_after_turn():
    assert direction_after_turn(UP, "left") == LEFT
    assert direction_after_turn(UP, "right") == RIGHT

    assert direction_after_turn(RIGHT, "left") == UP
    assert direction_after_turn(RIGHT, "right") == DOWN

    assert direction_after_turn(DOWN, "left") == RIGHT
    assert direction_after_turn(DOWN, "right") == LEFT

    assert direction_after_turn(LEFT, "left") == DOWN
    assert direction_after_turn(LEFT, "right") == UP

def test_turn():
    snake = Snake()

    initial_dir = snake.dir
    snake.turn("left")

    assert snake.dir == direction_after_turn(initial_dir, "left")

    snake.turn("right")
    assert snake.dir == initial_dir

    snake.turn("right")
    assert snake.dir == direction_after_turn(initial_dir, "right")

def test_get_free_random_position():

    snake = Snake()

    fake_position = (2, 3)

    with patch("random.choice", return_value=fake_position):
        assert snake._get_free_random_position() == fake_position

def free_positions_integrity(snake):

    # Vérifie que chaque élément de free_positions n'est pas dans le snake
    for pos in snake.free_positions:
        assert pos not in snake.positions
        assert pos not in snake.green_apple_positions
        assert pos not in snake.red_apple_positions

    # Vérifie que l'union de toutes les positions couvre bien tout le board
    all_positions = set((x, y) for x in range(10) for y in range(10))
    assert snake.free_positions | set(snake.positions) | snake.green_apple_positions | snake.red_apple_positions == all_positions

def test_place_apples():
    snake = Snake()
    free_positions_integrity(snake)

    apple_placed = True
    iteration = 0  # Pour suivre le nombre de placements

    while apple_placed:
        print(f"Iteration {iteration}")
        green_apples_positions = snake.green_apple_positions.copy()
        free_positions_copy = snake.free_positions.copy()

        apple_placed = snake._place_apples(1, "green")
        free_positions_integrity(snake)  # Vérifie l'intégrité après chaque placement

        if apple_placed:
            new_green_apple_position = list(snake.green_apple_positions - green_apples_positions)[0]
            assert new_green_apple_position in free_positions_copy, f"Erreur : pomme placée hors free_positions à l'itération {iteration}"

        iteration += 1

    # Vérifie bien que le jeu détecte la fin
    assert not apple_placed, f"Erreur : _place_apples aurait dû retourner False quand le board est plein à l'itération {iteration}"

def test_next_pos():
    snake = Snake()

    assert snake.next_pos((0, 0), UP) == (-1, 0)
    assert snake.next_pos((0, 0), RIGHT) == (0, 1)
    assert snake.next_pos((0, 0), DOWN) == (1, 0)
    assert snake.next_pos((0, 0), LEFT) == (0, -1)

    with pytest.raises(ValueError):
        snake.next_pos((0, 0), 99)

    with pytest.raises(ValueError):
        snake.next_pos((0, 0), -1)

    with pytest.raises(ValueError):
        snake.next_pos((0, 0), "up")

def test_tile_type():
    snake = Snake()
    snake.positions = []
    snake.green_apple_positions = set()
    snake.red_apple_positions = set()

    assert snake.tile_type((0, 0)) == "empty"
    assert snake.tile_type((0, 1)) == "empty"
    assert snake.tile_type((1, 1)) == "empty"

    snake.positions = [(0, 0), (0, 1), (1, 1)]
    assert snake.tile_type((0, 0)) == "snake"
    assert snake.tile_type((0, 1)) == "snake"
    assert snake.tile_type((1, 1)) == "snake"

    snake.green_apple_positions = {(2, 2)}
    assert snake.tile_type((2, 2)) == "green"
    assert snake.tile_type((2, 1)) == "empty"
    assert snake.tile_type((1, 1)) == "snake"

    snake.red_apple_positions = {(3, 1)}
    assert snake.tile_type((2, 2)) == "green"
    assert snake.tile_type((3, 1)) == "red"
    assert snake.tile_type((1, 1)) == "snake"

    assert snake.tile_type((-1, 5)) == "wall"
    assert snake.tile_type((5, -1)) == "wall"
    assert snake.tile_type((10, 5)) == "wall"
    assert snake.tile_type((5, 10)) == "wall"

# Assume that next_position is legal
@pytest.mark.parametrize("pos, dir", [
    ((5,5), UP),
    ((5,5), DOWN),
    ((5,5), LEFT),
    ((5,5), RIGHT),
])
def test_insert_head(pos, dir):
    state = {
        "positions": [pos],
        "dir": dir,
        "green_apples": [],
        "red_apples": [],
    }
    snake = Snake(state=state)
    snake.positions = [pos]
    snake.dir = dir

    new_head = snake.next_pos(snake.positions[0], snake.dir)
    snake._insert_head(new_head)

    assert snake.positions[0] == new_head
    free_positions_integrity(snake)

def test_pop_tail():
    snake = Snake()
    positions = snake.positions.copy()
    snake._pop_tail()

    assert snake.positions == positions[:-1]

