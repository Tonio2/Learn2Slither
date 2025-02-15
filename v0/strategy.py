from snake import  direction_after_turn, DIRECTIONS

def compute_danger(snake):
    head = snake.positions[0]
    x, y = head
    dirs = [direction_after_turn(snake.dir, "left"), direction_after_turn(snake.dir, "right"), snake.dir]
    tiles = [(x + DIRECTIONS[dir][0], y + DIRECTIONS[dir][1]) for dir in dirs]
    dangers = [0, 0, 0]
    for i, tile in enumerate(tiles):
        if tile in snake.positions or tile[0] < 0 or tile[0] >= snake.board_size or tile[1] < 0 or tile[1] >= snake.board_size:
            dangers[i] = 1
    return dangers


def state_to_index(snake):
    [danger_left, danger_right, danger_center] = compute_danger(snake)
    return danger_left * 2**2 + danger_right * 2 + danger_center


# We notice that the table could converge really fast to the optimal solution
# But because it gets a -500 when it dies from eating a red apple as well as hitting a wall, sometimes, some path can be not perfectly exact
# We can test it now

# Also the last state is never reached, which make sense
# Because it's rare to have danger left, right and center at the same time
