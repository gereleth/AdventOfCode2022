# Day 23: Unstable Diffusion
# Problem statement: https://adventofcode.com/2022/day/23

import numpy as np
from matplotlib import pyplot as plt
from collections import Counter

day_title = "Unstable Diffusion"

EMPTY = 0
ELF = 1

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
STAY = 16

DELTAS = {
    # (dy, dx)
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1),
    NORTH: (-1, 0),
}


def parse_board(text):
    lines = text.split("\n")
    H = len(lines)
    W = len(lines[0])
    padding = 30
    board = np.zeros((2 * padding + H, 2 * padding + W), dtype=np.int8)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                board[padding + y, padding + x] = ELF
    return board


def slice(board, direction):
    if direction == NORTH:
        return board[:-2, 1:-1]
    elif direction == NORTH + EAST:
        return board[:-2, 2:]
    elif direction == NORTH + WEST:
        return board[:-2, :-2]
    elif direction == SOUTH:
        return board[2:, 1:-1]
    elif direction == SOUTH + WEST:
        return board[2:, :-2]
    elif direction == SOUTH + EAST:
        return board[2:, 2:]
    elif direction == WEST:
        return board[1:-1, :-2]
    elif direction == EAST:
        return board[1:-1, 2:]


def count_empty_tiles(board):
    yy, xx = np.nonzero(board)
    ymin, ymax = yy.min(), yy.max()
    xmin, xmax = xx.min(), xx.max()
    return (board[ymin : ymax + 1, xmin : xmax + 1] == EMPTY).sum()


def simulate(board, rounds=0):
    iter_limit = rounds if rounds > 0 else np.Inf
    N = board.sum() / ELF
    directions = [NORTH, SOUTH, WEST, EAST]
    d = 0
    iteration = 0
    while iteration < iter_limit:
        iteration += 1
        propose = np.zeros_like(board[1:-1, 1:-1])

        # stay in place if noone is around
        stay_in_place = (
            sum(
                slice(board, direction)
                for direction in [
                    NORTH,
                    NORTH + EAST,
                    EAST,
                    EAST + SOUTH,
                    SOUTH,
                    SOUTH + WEST,
                    WEST,
                    NORTH + WEST,
                ]
            )
            == 0
        )
        propose[stay_in_place] = STAY

        # propose moving in directions
        for nd in range(4):
            direction = directions[(d + nd) % 4]

            if direction in (NORTH, SOUTH):
                bb = (
                    slice(board, direction)
                    + slice(board, direction + WEST)
                    + slice(board, direction + EAST)
                )
            else:
                bb = (
                    slice(board, direction)
                    + slice(board, direction + SOUTH)
                    + slice(board, direction + NORTH)
                )
            can_move = (propose == 0) & (board[1:-1, 1:-1] > 0) & (bb == 0)
            propose[can_move] = direction
            if (propose > 0).sum() == N:
                break

        # collect source and destination of each proposed move
        propose[stay_in_place] = 0
        moves = []
        for y, x in np.argwhere(propose):
            direction = propose[y, x]
            dy, dx = DELTAS[direction]
            moves.append((1 + y, 1 + x, 1 + y + dy, 1 + x + dx))

        # move if noone else is moving there
        destination_counts = Counter((m[2], m[3]) for m in moves)
        moved = False
        extend_directions = set()  # in case we get outside initial bounds
        for y0, x0, y1, x1 in moves:
            if destination_counts[(y1, x1)] > 1:
                continue
            board[y0, x0] -= ELF
            board[y1, x1] += ELF
            moved = True
            if y1 == 0:
                extend_directions.add(NORTH)
            if y1 == board.shape[0] - 1:
                extend_directions.add(SOUTH)
            if x1 == 0:
                extend_directions.add(WEST)
            if x1 == board.shape[1] - 1:
                extend_directions.add(EAST)

        # extend the borders if necessary:
        if len(extend_directions) > 0:
            rows = max(20, board.shape[0] // 2)
            rows_above = rows if NORTH in extend_directions else 0
            rows_below = rows if SOUTH in extend_directions else 0
            cols = max(20, board.shape[1] // 2)
            cols_left = cols if WEST in extend_directions else 0
            cols_right = cols if EAST in extend_directions else 0
            new_board = np.zeros(
                (
                    board.shape[0] + rows_above + rows_below,
                    board.shape[1] + cols_left + cols_right,
                ),
                dtype=board.dtype,
            )
            new_board[
                rows_above : rows_above + board.shape[0],
                cols_left : cols_left + board.shape[1],
            ] = board
            board = new_board

        # switch directions order for the next round
        d = (d + 1) % 4
        if not moved:
            break
    return board, iteration


def part1(text_input):
    board = parse_board(text_input)
    board, _ = simulate(board, rounds=10)
    return count_empty_tiles(board)


def part2(text_input):
    board = parse_board(text_input)
    board, iteration = simulate(board, rounds=0)
    return iteration
