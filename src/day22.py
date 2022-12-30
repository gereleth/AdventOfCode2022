# Day 22: Monkey Map
# Problem statement: https://adventofcode.com/2022/day/22

from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import re

day_title = "Monkey Map"

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


class WrappingBoard:
    def __init__(self, board):
        self.board = board
        # find out cube side length
        self.size = int(np.sqrt((board != VOID).sum() // 6))

    def whats_ahead(self, x, y, direction):
        dy, dx = DELTAS[direction]
        nx = (x + dx) % self.board.shape[1]
        ny = (y + dy) % self.board.shape[0]
        while self.board[ny, nx] == VOID:
            nx = (nx + self.size * dx) % self.board.shape[1]
            ny = (ny + self.size * dy) % self.board.shape[0]
        return nx, ny, direction, self.board[ny, nx]


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


def follow_path(geometry, moves, return_path=False):
    y = 0
    x = next(i for i, cell in enumerate(geometry.board[0]) if cell == EMPTY)
    direction = RIGHT
    moves = re.findall(r"(\d+|L|R)", moves.strip())
    if return_path:
        xx = [x]
        yy = [y]
    for move in moves:
        if move == "L":
            direction = (direction - 1) % 4
        elif move == "R":
            direction = (direction + 1) % 4
        else:
            steps = int(move)
            for _ in range(steps):
                nx, ny, ndirection, next_cell = geometry.whats_ahead(x, y, direction)
                if next_cell == EMPTY:
                    x = nx
                    y = ny
                    direction = ndirection
                    if return_path:
                        xx.append(x)
                        yy.append(y)
                elif next_cell == WALL:
                    break
    if return_path:
        return xx, yy
    else:
        return x, y, direction


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

    def whats_ahead(self, x, y, direction):
        dy, dx = DELTAS[direction]
        nx = x + dx
        ny = y + dy
        ndir = direction
        if nx < 0 or nx >= self.board.shape[1] or ny < 0 or ny >= self.board.shape[0]:
            # tried to go out of bounds
            next_cell = VOID
        else:
            next_cell = self.board[ny, nx]
        if next_cell != VOID:
            return nx, ny, ndir, next_cell
        # stepped into the void, have to wrap around
        coord = (y // self.size, x // self.size)
        face = self.loc_to_face[coord]
        wrap_face, wrap_direction, wrap_switch = self.wrap(face, direction)
        if direction in (UP, DOWN):
            source_coord = x - self.size * self.faces[face]["x"]
        else:
            source_coord = y - self.size * self.faces[face]["y"]
        if wrap_switch:
            source_coord = self.size - 1 - source_coord
        wy = self.size * self.faces[wrap_face]["y"]
        wx = self.size * self.faces[wrap_face]["x"]
        ndir = wrap_direction
        if wrap_direction == RIGHT:
            nx = wx
            ny = wy + source_coord
        elif wrap_direction == DOWN:
            nx = wx + source_coord
            ny = wy
        elif wrap_direction == LEFT:
            nx = wx + self.size - 1
            ny = wy + source_coord
        elif wrap_direction == UP:
            nx = wx + source_coord
            ny = wy + self.size - 1
        else:
            raise ValueError("unknown wrap direction")
        next_cell = self.board[ny, nx]
        return nx, ny, ndir, next_cell


def part1(text_input):
    board, moves = text_input.split("\n\n")
    board = parse_board(board)
    geometry = WrappingBoard(board)
    x, y, direction = follow_path(geometry, moves)
    return 1000 * (y + 1) + 4 * (x + 1) + direction


def part2(text_input):
    board, moves = text_input.split("\n\n")
    board = parse_board(board)
    geometry = Cube(board)
    x, y, direction = follow_path(geometry, moves)
    return 1000 * (y + 1) + 4 * (x + 1) + direction


def visualize(text_input):
    board, moves = text_input.split("\n\n")
    board = parse_board(board)
    geometry = Cube(board)
    xx, yy = follow_path(geometry, moves, return_path=True)
    x_cube = np.array(xx)
    y_cube = np.array(yy)

    geometry = WrappingBoard(board)
    xx, yy = follow_path(geometry, moves, return_path=True)
    x_wrap = np.array(xx)
    y_wrap = np.array(yy)

    fig, ax = plt.subplots(figsize=(12, 16), facecolor="black")
    ax.axis("off")
    ax.set(facecolor="black")
    b = np.zeros_like(board)
    b[board == VOID] = -10
    b[board == EMPTY] = 10
    b[board == WALL] = 4
    ax.imshow(b, cmap="gray", vmax=15)
    (line_wrap,) = ax.plot(
        x_wrap[:10], y_wrap[:10], color="C0", zorder=10, lw=0, marker="o", ms=12
    )
    (line_cube,) = ax.plot(
        x_cube[:10], y_cube[:10], color="C3", zorder=10, lw=0, marker="o", ms=12
    )
    # Show where cube sides wrap
    # Patches are specific to my task input
    # I was too lazy to draw them in a general way
    patches = [
        Rectangle((50 - 0.5, 0 - 0.5 - 3), 50, 3, color="C0"),
        Rectangle((-3 - 0.5, 150 - 0.5), 3, 50, color="C0"),
        Rectangle((50 - 3 - 0.5, 0 - 0.5), 3, 50, color="C1"),
        Rectangle((-3 - 0.5, 100 - 0.5), 3, 50, color="C1"),
        Rectangle((50 - 3 - 0.5, 50 - 0.5), 3, 50, color="C2"),
        Rectangle((0 - 0.5, 100 - 0.5 - 3), 50, 3, color="C2"),
        Rectangle((100 - 0.5, 0 - 0.5 - 3), 50, 3, color="C3"),
        Rectangle((0 - 0.5, 200 - 0.5), 50, 3, color="C3"),
        Rectangle((150 - 0.5, 0 - 0.5), 3, 50, color="C4"),
        Rectangle((100 - 0.5, 100 - 0.5), 3, 50, color="C4"),
        Rectangle((100 - 0.5, 50 - 0.5), 3, 50, color="C2"),
        Rectangle((100 - 0.5, 50 - 0.5), 50, 3, color="C2"),
        Rectangle((50 - 0.5, 150 - 0.5), 3, 50, color="C2"),
        Rectangle((50 - 0.5, 150 - 0.5), 50, 3, color="C2"),
    ]
    ax.add_collection(PatchCollection(patches, match_original=True))
    ax.autoscale_view()

    def animate(i):
        line_wrap.set(
            xdata=x_wrap[max(0, i - 20) : min(i, len(x_wrap))],
            ydata=y_wrap[max(0, i - 20) : min(i, len(x_wrap))],
        )  # update the data.
        line_cube.set(
            xdata=x_cube[max(0, i - 20) : min(i, len(x_cube))],
            ydata=y_cube[max(0, i - 20) : min(i, len(x_cube))],
        )
        return (
            line_wrap,
            line_cube,
        )

    fig.tight_layout()
    ani = animation.FuncAnimation(fig, animate, interval=10, blit=True, save_count=2000)

    # writer = animation.FFMpegWriter(fps=30, metadata=dict(artist="me"), bitrate=1800)
    # ani.save("day_22.mp4", writer=writer)

    plt.show()


if __name__ == "__main__":
    folder = Path(__file__).parent.parent
    with open(folder / "inputs" / "day22" / "task.txt") as f:
        content = f.read().rstrip()
    visualize(content)
