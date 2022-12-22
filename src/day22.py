# Day 22: Monkey Map
# Problem statement: https://adventofcode.com/2022/day/22

import numpy as np
import re

EMPTY = 0
VOID = -1
WALL = 1

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

DELTAS = [
    # (dy, dx)
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
    (-1, 0),  # up
]

X = "x"
Y = "y"
Z = "z"


def parse_board(text):
    lines = text.split("\n")
    H = len(lines)
    W = max(len(line) for line in lines)
    board = np.zeros((H, W), dtype=np.int8) + VOID
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                board[y, x] = EMPTY
            elif char == "#":
                board[y, x] = WALL
            # else leave as VOID
    return board


def part1(text_input):
    board, moves = text_input.split("\n\n")
    board = parse_board(board)
    y = 0
    x = next(i for i, cell in enumerate(board[0]) if cell == EMPTY)
    direction = RIGHT
    moves = re.findall(r"(\d+|L|R)", moves.strip())
    for move in moves:
        if move == "L":
            direction = (direction - 1) % 4
        elif move == "R":
            direction = (direction + 1) % 4
        else:
            steps = int(move)
            dy, dx = DELTAS[direction]
            for _ in range(steps):
                nx = x
                ny = y
                while True:
                    nx = (nx + dx) % board.shape[1]
                    ny = (ny + dy) % board.shape[0]
                    next_cell = board[ny, nx]
                    if next_cell != VOID:
                        break
                if next_cell == EMPTY:
                    x = nx
                    y = ny
                elif next_cell == WALL:
                    break
    return 1000 * (y + 1) + 4 * (x + 1) + direction


class Cube:
    def __init__(self, board):
        self.board = board
        # find out cube side length
        self.size = int(np.sqrt((board != VOID).sum() // 6))
        self.loc_to_face = {}
        self.faces = {}
        # index cube faces
        current_face = 0
        for y in range(board.shape[0] // self.size):
            for x in range(board.shape[1] // self.size):
                if board[y * self.size + 1, x * self.size + 1] == VOID:
                    continue
                self.loc_to_face[(y, x)] = current_face
                self.faces[current_face] = dict(x=x, y=y)
                current_face += 1
        # figure out wrapping...
        # position face 0 in plane z==0 and set edges
        # so that left-right is x=0 to x=1
        # and up-down is y=0 to y=1
        self.faces[0]["plane"] = (Z, 0)
        self.faces[0]["edges"] = [(X, 1), (Y, 1), (X, 0), (Y, 0)]
        # After setting one face arbitrarily the rest can be determined uniquely
        check_faces = set([0])
        while len(check_faces) > 0:
            face = check_faces.pop()
            x, y = self.faces[face]["x"], self.faces[face]["y"]
            for direction, (dy, dx) in enumerate(DELTAS):
                if (y + dy, x + dx) not in self.loc_to_face:
                    continue
                other = self.loc_to_face[(y + dy, x + dx)]
                if "plane" in self.faces[other]:
                    continue
                self.faces[other]["plane"] = self.faces[face]["edges"][direction]
                self.faces[other]["edges"] = [None] * 4
                d = (direction - 1) % 4
                self.faces[other]["edges"][d] = self.faces[face]["edges"][d]
                d = (direction + 1) % 4
                self.faces[other]["edges"][d] = self.faces[face]["edges"][d]
                d = (direction + 2) % 4  # opposite
                plane = self.faces[face]["plane"]
                self.faces[other]["edges"][d] = plane
                self.faces[other]["edges"][direction] = (plane[0], 1 - plane[1])
                check_faces.add(other)

    def wrap(self, face_index, direction):
        # from where
        face = self.faces[face_index]
        plane = face["plane"]
        edge = face["edges"][direction]
        perpendicular_direction = (direction + 1) % 4
        if perpendicular_direction in (UP, DOWN):
            sign = face["edges"][DOWN][1] - face["edges"][UP][1]
        else:
            sign = face["edges"][RIGHT][1] - face["edges"][LEFT][1]
        # to where
        other_face_index = next(i for i, f in self.faces.items() if f["plane"] == edge)
        other_face = self.faces[other_face_index]
        opposite_other = other_face["edges"].index(plane)
        other_direction = (opposite_other + 2) % 4
        perpendicular_direction = (other_direction + 1) % 4
        if perpendicular_direction in (UP, DOWN):
            other_sign = other_face["edges"][DOWN][1] - other_face["edges"][UP][1]
        else:
            other_sign = other_face["edges"][RIGHT][1] - other_face["edges"][LEFT][1]
        return other_face_index, other_direction, sign != other_sign

    def which_face(self, x, y):
        coord = (y // self.size, x // self.size)
        return self.loc_to_face[coord]

    def face_origin(self, face_index):
        wy = self.size * self.faces[face_index]["y"]
        wx = self.size * self.faces[face_index]["x"]
        return wy, wx


def part2(text_input):
    board, moves = text_input.split("\n\n")
    board = parse_board(board)
    cube = Cube(board)
    y = 0
    x = next(i for i, cell in enumerate(board[0]) if cell == EMPTY)
    direction = RIGHT
    moves = re.findall(r"(\d+|L|R)", moves.strip())
    for move in moves:
        if move == "L":
            direction = (direction - 1) % 4
        elif move == "R":
            direction = (direction + 1) % 4
        else:
            steps = int(move)
            dy, dx = DELTAS[direction]
            for _ in range(steps):
                nx = x + dx
                ny = y + dy
                ndir = direction
                if nx < 0 or nx >= board.shape[1] or ny < 0 or ny >= board.shape[0]:
                    # tried to go out of bounds
                    next_cell = VOID
                else:
                    next_cell = board[ny, nx]
                if next_cell == VOID:
                    # have to wrap around
                    face = cube.which_face(x, y)
                    wrap_face, wrap_direction, wrap_switch = cube.wrap(face, direction)
                    if direction in (UP, DOWN):
                        source_coord = x - cube.size * cube.faces[face]["x"]
                    else:
                        source_coord = y - cube.size * cube.faces[face]["y"]
                    if wrap_switch:
                        source_coord = cube.size - 1 - source_coord
                    wy, wx = cube.face_origin(wrap_face)
                    ndir = wrap_direction
                    if wrap_direction == RIGHT:
                        nx = wx
                        ny = wy + source_coord
                    elif wrap_direction == DOWN:
                        nx = wx + source_coord
                        ny = wy
                    elif wrap_direction == LEFT:
                        nx = wx + cube.size - 1
                        ny = wy + source_coord
                    elif wrap_direction == UP:
                        nx = wx + source_coord
                        ny = wy + cube.size - 1
                    else:
                        raise ValueError("unknown wrap direction")
                    next_cell = board[ny, nx]
                if next_cell == EMPTY:
                    x = nx
                    y = ny
                    direction = ndir
                    dy, dx = DELTAS[direction]
                elif next_cell == WALL:
                    break
                else:
                    raise ValueError("got void cell after wrapping")
    return 1000 * (y + 1) + 4 * (x + 1) + direction


def run(input_path):
    print("Day 22: Monkey Map")
    with open(input_path) as f:
        content = f.read()
    print("Part 1:", part1(content))
    print("Part 2:", part2(content))
