# Day 17: Pyroclastic Flow
# Problem statement: https://adventofcode.com/2022/day/17

import numpy as np


day_title = "Pyroclastic Flow"

BLOCKS = [
    np.array([[1, 1, 1, 1]], dtype=np.int8),
    2
    * np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        dtype=np.int8,
    ),
    3  # L block looks rotated because in my numpy implementation rocks fall up))
    * np.array(
        [
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ],
        dtype=np.int8,
    ),
    4
    * np.array(
        [
            [1],
            [1],
            [1],
            [1],
        ],
        dtype=np.int8,
    ),
    5
    * np.array(
        [
            [1, 1],
            [1, 1],
        ],
        dtype=np.int8,
    ),
]

WINDS_DX = {"<": -1, ">": 1}


class Tetris:
    def __init__(self, wind_pattern, width=7):
        self.width = width
        self.wind_pattern = wind_pattern
        self.tower = np.zeros((1000, width), dtype=np.int8)
        self.highest = 0
        self.wind_index = 0
        self.block_index = 0

    def get_block(self):
        shape = BLOCKS[self.block_index]
        self.block_index = (self.block_index + 1) % len(BLOCKS)
        return shape

    def get_wind_dx(self):
        wind = self.wind_pattern[self.wind_index]
        self.wind_index = (self.wind_index + 1) % len(self.wind_pattern)
        return WINDS_DX[wind]

    def is_blocked(self, block, x, y):
        """Check if block with lower left corner at x,y intersects walls or the tower"""
        if x < 0 or x + block.shape[1] > self.width or y < 0:
            return True
        return np.any(
            self.tower[y : y + block.shape[0], x : x + block.shape[1]] * block > 0
        )

    def drop_block(self):
        block = self.get_block()
        x = 2
        y = self.highest + 3
        while True:
            dx = self.get_wind_dx()
            if self.is_blocked(block, x + dx, y):
                dx = 0
            x = x + dx
            if self.is_blocked(block, x, y - 1):
                break
            else:
                y = y - 1
        self.tower[y : y + block.shape[0], x : x + block.shape[1]] += block
        self.highest = max(self.highest, y + block.shape[0])
        if self.highest + 10 >= self.tower.shape[0]:
            self.tower = np.vstack(((self.tower, np.zeros_like(self.tower))))

    def to_str(self, top_rows=30):
        res = []
        for row in self.tower[max(0, self.highest - top_rows) : self.highest + 1, :][
            ::-1, :
        ]:
            res.append("".join("#" if value > 0 else "." for value in row))
        return "\n".join(res)


def history_aware_drop(tetris: Tetris, rounds=2022, top_rows=30):
    i = 0
    # state_index: (round, height, top_rows_string)
    seen = {}
    repeated_height = 0
    cannot_repeat = len(BLOCKS) * len(tetris.wind_pattern) >= rounds
    while i < rounds:
        i += 1
        tetris.drop_block()
        if cannot_repeat or repeated_height > 0 or tetris.highest < top_rows:
            continue
        state_index = tetris.block_index + len(BLOCKS) * tetris.wind_index
        (r, h, top) = seen.get(state_index, (None, None, None))
        current_top = tetris.to_str(top_rows=top_rows)
        if current_top == top:
            delta_rounds = i - r
            delta_height = tetris.highest - h
            rounds_left = rounds - i
            repeats = rounds_left // delta_rounds
            i += repeats * delta_rounds
            repeated_height = repeats * delta_height
        seen[state_index] = (i, tetris.highest, current_top)
    return tetris.highest + repeated_height


def part1(text_input):
    tetris = Tetris(text_input)
    for _ in range(2022):
        tetris.drop_block()
    return tetris.highest


def part2(text_input):
    tetris = Tetris(text_input)
    return history_aware_drop(tetris, rounds=1000000000000)
