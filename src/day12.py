# Day 12: Hill Climbing Algorithm
# Problem statement: https://adventofcode.com/2022/day/12

import math
from collections import namedtuple
import heapq
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from matplotlib import transforms

day_title = "Hill Climbing Algorithm"

DELTAS = {
    # (dy, dx)
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
    "^": (-1, 0),
}

State = namedtuple("State", ["turn", "x", "y", "path"])


def parse_heights(text_input):
    heights = []
    start = None
    finish = None
    for y, line in enumerate(text_input.split()):
        row = []
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
                row.append(0)
            elif char == "E":
                finish = (x, y)
                row.append(ord("z") - 97)
            else:
                row.append(ord(char) - 97)
        heights.append(row)
    return heights, start, finish


class Hills:
    def __init__(self, text_input):
        # switch start and finish because search is faster this way for the tasks
        self.heights, self.finish, self.start = parse_heights(text_input)
        self.min_steps = {}

    def next_states(self, state: State):
        x, y = state.x, state.y
        for direction, (dy, dx) in DELTAS.items():
            xnew, ynew = x + dx, y + dy
            if xnew < 0 or xnew >= len(self.heights[0]):
                continue
            if ynew < 0 or ynew >= len(self.heights):
                continue
            if self.heights[y][x] - self.heights[ynew][xnew] > 1:
                continue
            steps = self.min_steps.get((xnew, ynew), math.inf)
            if len(state.path) + 1 >= steps:
                continue
            self.min_steps[(xnew, ynew)] = len(state.path) + 1
            yield State(state.turn + 1, xnew, ynew, state.path + direction)


def search_1(hills: Hills, yield_search_states=False):
    queue = [(0, State(0, *hills.start, ""))]
    heapq.heapify(queue)
    bestpath = ""
    bestlen = math.inf
    while len(queue) > 0:
        _, prev_state = heapq.heappop(queue)
        if yield_search_states:
            yield prev_state.path
        for state in hills.next_states(prev_state):
            if (state.x, state.y) == hills.finish:
                if len(state.path) < bestlen:
                    bestpath = state.path
                    bestlen = len(state.path)
                    if yield_search_states:
                        yield state.path
            else:
                lower_bound = (
                    state.turn
                    + abs(state.x - hills.finish[0])
                    + abs(state.y - hills.finish[1])
                )
                if lower_bound >= bestlen:
                    continue
                heapq.heappush(queue, (lower_bound, state))
    yield bestpath


def part1(text_input: str):
    hills = Hills(text_input)
    bestpath = next(search_1(hills))
    return len(bestpath)


def search_2(hills: Hills, yield_search_states=False):
    queue = [(0, State(0, *hills.start, ""))]
    heapq.heapify(queue)
    bestpath = ""
    bestlen = math.inf
    while len(queue) > 0:
        _, prev_state = heapq.heappop(queue)
        if yield_search_states:
            yield prev_state.path
        for state in hills.next_states(prev_state):
            if hills.heights[state.y][state.x] == 0:
                if len(state.path) < bestlen:
                    bestpath = state.path
                    bestlen = len(state.path)
                    if yield_search_states:
                        yield state.path
            else:
                lower_bound = state.turn + hills.heights[state.y][state.x]
                if lower_bound >= bestlen:
                    continue
                heapq.heappush(queue, (lower_bound, state))
    yield bestpath


def part2(text_input: str):
    hills = Hills(text_input)
    bestpath = next(search_2(hills))
    return len(bestpath)


def path_to_xydata(path, x0, y0):
    x, y = x0, y0
    xx, yy = [x], [y]
    for char in path:
        dy, dx = DELTAS[char]
        x += dx
        y += dy
        xx.append(x)
        yy.append(y)
    return dict(xdata=xx, ydata=yy)


def visualize(text_input: str, iterations_per_frame=10):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 9), facecolor="#333")
    ax1.set_title("Part 1", color="#ccc")
    ax2.set_title("Part 2", color="#ccc")
    ax1.axis("off")
    ax2.axis("off")

    hills_1 = Hills(text_input)
    hills_2 = Hills(text_input)

    ax1.imshow(hills_1.heights, interpolation="none", cmap="gray", aspect="auto")
    ax2.imshow(hills_1.heights, interpolation="none", cmap="gray", aspect="auto")
    h1 = [[math.nan] * len(hills_1.heights[0]) for _ in hills_1.heights]
    h2 = [[math.nan] * len(hills_1.heights[0]) for _ in hills_1.heights]
    im1 = ax1.imshow(h1, cmap="viridis", vmin=0, vmax=26)
    im2 = ax2.imshow(h2, cmap="viridis", vmin=0, vmax=26)
    ax1.add_patch(
        Circle(
            (hills_1.start[0], hills_1.start[1]),
            radius=0.3,
            facecolor="C1",
            lw=1,
        )
    )
    ax1.add_patch(
        Circle(
            (hills_1.finish[0], hills_1.finish[1]),
            radius=0.3,
            facecolor="C1",
            lw=1,
        )
    )
    ax2.add_patch(
        Circle(
            (hills_2.start[0], hills_2.start[1]),
            radius=0.3,
            facecolor="C1",
            lw=1,
        )
    )
    (trail1,) = ax1.plot([], [], "-", lw=2, color="C1")
    (trail2,) = ax2.plot([], [], "-", lw=2, color="C1")
    search1 = search_1(hills_1, yield_search_states=True)
    search2 = search_2(hills_2, yield_search_states=True)

    def animate(i):
        nonlocal search1, search2, h1
        if i == 0:
            search1 = search_1(hills_1, yield_search_states=True)
            trail1.set(xdata=[], ydata=[])
            search2 = search_2(hills_2, yield_search_states=True)
            trail2.set(xdata=[], ydata=[])
        else:
            try:
                for _ in range(iterations_per_frame):
                    path = next(search1)
                    data = path_to_xydata(path, *hills_1.start)
                    x, y = data["xdata"][-1], data["ydata"][-1]
                    h1[y][x] = hills_1.heights[y][x]
                    im1.set_array(h1)
                    trail1.set(**data)
            except StopIteration:
                pass
            try:
                for _ in range(iterations_per_frame):
                    path = next(search2)
                    data = path_to_xydata(path, *hills_2.start)
                    x, y = data["xdata"][-1], data["ydata"][-1]
                    h2[y][x] = hills_1.heights[y][x]
                    im2.set_array(h2)
                    trail2.set(**data)
            except StopIteration:
                pass

        return (trail1, trail2, im1, im2)

    fig.tight_layout()

    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=50,
        blit=False,
        # frames=24 * 18,
        # repeat_delay=3000,
    )

    # writer = animation.FFMpegWriter(fps=12, metadata=dict(artist="me"), bitrate=1800)
    # ani.save("day_12.mp4", writer=writer)

    plt.show()


if __name__ == "__main__":
    folder = Path(__file__).parent.parent
    with open(folder / "inputs" / "day12" / "test.txt") as f:
        content = f.read().rstrip()
    visualize(content, iterations_per_frame=10)
