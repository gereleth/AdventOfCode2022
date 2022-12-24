# Day 24: Blizzard Basin
# Problem statement: https://adventofcode.com/2022/day/24

import numpy as np

from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from collections import namedtuple, defaultdict
from matplotlib import rcParams
import heapq

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
WAIT = 4

DELTAS = {
    # (dy, dx)
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1),
    NORTH: (-1, 0),
    WAIT: (0, 0),
}

PATHCHARS = {
    EAST: ">",
    SOUTH: "v",
    WEST: "<",
    NORTH: "^",
    WAIT: ".",
}

CHARDIRECTIONS = {char: direction for direction, char in PATHCHARS.items()}

Blizzard = namedtuple("Blizzard", ["x", "y", "direction"])


def parse_board(text):
    lines = text.split("\n")

    bounds = (1, len(lines[0]) - 2, 1, len(lines) - 2)
    blizzards = [
        Blizzard(x, y, CHARDIRECTIONS[char])
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char not in ".#"
    ]
    return blizzards, bounds


class Winds:
    def __init__(self, blizzards, xmin, xmax, ymin, ymax):
        self.pos = defaultdict(set)
        for blizzard in blizzards:
            self.pos[(blizzard.x, blizzard.y)].add(blizzard)
        self.free_spots_cache = []
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def _winds_flow(self):
        pos = defaultdict(set)
        for blizzards in self.pos.values():
            for b in blizzards:
                dy, dx = DELTAS[b.direction]
                nx, ny = b.x + dx, b.y + dy
                if nx < self.xmin:
                    nx = self.xmax
                elif nx > self.xmax:
                    nx = self.xmin
                if ny < self.ymin:
                    ny = self.ymax
                elif ny > self.ymax:
                    ny = self.ymin
                pos[(nx, ny)].add(Blizzard(nx, ny, b.direction))
        self.pos = pos

    def get_free_spots(self, turn):
        if turn < len(self.free_spots_cache):
            return self.free_spots_cache[turn]
        while turn >= len(self.free_spots_cache):
            self._winds_flow()
            # print(self.flows_str())
            free = set(((self.xmax, self.ymax + 1), (self.xmin, self.ymin - 1)))
            for x in range(self.xmin, self.xmax + 1):
                for y in range(self.ymin, self.ymax + 1):
                    if (x, y) not in self.pos:
                        free.add((x, y))
            self.free_spots_cache.append(free)
        return self.free_spots_cache[turn]

    def is_free(self, pos):
        if (pos.x, pos.y) == (self.xmin, self.ymin - 1):
            return True
        if (pos.x, pos.y) == (self.xmax, self.ymax + 1):
            return True
        free = self.get_free_spots(pos.turn)
        return (pos.x, pos.y) in free

    def flows_str(self):
        res = []
        for y in range(self.ymin, self.ymax + 1):
            line = []
            for x in range(self.xmin, self.xmax + 1):
                f = self.pos.get((x, y), None)
                if f is None:
                    line.append(".")
                elif len(f) == 1:
                    line.append(PATHCHARS[next(iter(f)).direction])
                else:
                    line.append(str(len(f)))
            res.append("".join(line))
        return "\n".join(res)

    def free_str(self, turn, xe, ye):
        free = self.get_free_spots(turn)
        res = []
        for y in range(self.ymin, self.ymax + 1):
            line = []
            for x in range(self.xmin, self.xmax + 1):
                if (x, y) == (xe, ye):
                    line.append("E")
                elif (x, y) in free:
                    line.append(".")
                else:
                    line.append("0")
            res.append("".join(line))
        return "\n".join(res)


SearchPosition = namedtuple("SearchPosition", ["x", "y", "turn"])


def find_best_path(winds, source, target, start_turn):
    queue = [(0, 0, SearchPosition(*source, start_turn), "")]
    heapq.heapify(queue)
    it = 0
    best_turns = -np.Inf
    best_path = ""
    visited = set()
    distance_x = abs(target[0] - source[0])
    distance_y = abs(target[1] - source[1])

    while len(queue) > 0:
        it += 1
        priority, _, pos, path = heapq.heappop(queue)
        turn = pos.turn + 1
        # print(f"Best {-best_turns} Options {len(queue)} Current {-priority} {pos}")
        for direction, (dy, dx) in DELTAS.items():
            npos = SearchPosition(pos.x + dx, pos.y + dy, turn)
            if npos in visited:
                continue
            if (npos.x, npos.y) == target:
                if turn < -best_turns:
                    best_turns = -turn
                    best_path = path + PATHCHARS[direction]
                    # print("BEST PATH", best_path, len(best_path), len(queue))
            elif winds.is_free(npos):
                newpath = path + PATHCHARS[direction]
                still_need_x = abs(target[0] - npos.x)
                still_need_y = abs(target[1] - npos.y)
                if npos.turn - start_turn + still_need_x + still_need_y >= -best_turns:
                    # print(f"\tposition {newpos} abandoned as useless")
                    continue
                # print(
                #     f"\tpush new position {MOVECHARS[direction]} {-priority} {newpos}"
                # )
                visited.add(npos)
                priority = -(
                    (distance_x - still_need_x + distance_y - still_need_y) * 1000
                    - (turn - start_turn)
                )
                heapq.heappush(queue, (priority, it, npos, newpath))
        # if it % 10000 == 0:
        #     print(
        #         f"it={it}\tqueue={len(queue)}\tbest={len(best_path)}\tvisited={len(visited)}"
        #     )
    return best_path


def part1(text_input):
    blizzards, bounds = parse_board(text_input)
    xmin, xmax, ymin, ymax = bounds
    winds = Winds(blizzards, *bounds)
    start = (xmin, ymin - 1)
    finish = (xmax, ymax + 1)
    best_path = find_best_path(winds, start, finish, -1)
    return len(best_path)


def part2(text_input):
    blizzards, bounds = parse_board(text_input)
    xmin, xmax, ymin, ymax = bounds
    winds = Winds(blizzards, *bounds)
    start = (xmin, ymin - 1)
    finish = (xmax, ymax + 1)
    there = find_best_path(winds, start, finish, -1)
    back = find_best_path(winds, finish, start, len(there) - 1)
    again = find_best_path(winds, start, finish, len(there) + len(back) - 1)
    return len(there) + len(back) + len(again)


def run(input_path):
    print("Day 24: Blizzard Basin")
    with open(input_path) as f:
        content = f.read()
    print("Part 1:", part1(content))
    print("Part 2:", part2(content))
    # visualize(content)


def visualize(text_input):
    blizzards, bounds = parse_board(text_input)
    xmin, xmax, ymin, ymax = bounds
    width = xmax - xmin + 1
    height = ymax - ymin + 1
    winds = Winds(blizzards, *bounds)
    start = (xmin, ymin - 1)
    finish = (xmax, ymax + 1)
    # path coordinates
    there = find_best_path(winds, start, finish, -1)
    back = find_best_path(winds, finish, start, len(there) - 1)
    again = find_best_path(winds, start, finish, len(there) + len(back) - 1)
    best_path = there + back + again
    xx, yy = [start[0]], [start[1]]
    x, y = start
    for char in best_path:
        dy, dx = DELTAS[CHARDIRECTIONS[char]]
        x, y = x + dx, y + dy
        xx.append(x)
        yy.append(y)
    # reinitialize winds to step through blizzard positions
    winds = Winds(blizzards, *bounds)
    wind_steps = []
    for i in range(len(best_path) + 2):
        step = defaultdict(lambda: ([], []))
        for _, blizzards in winds.pos.items():
            for b in blizzards:
                step[b.direction][0].append(b.x)
                step[b.direction][1].append(b.y)
        winds.get_free_spots(i)
        wind_steps.append(step)

    bgcolor = "dimgray"
    snowcolor = "white"
    wallcolor = "silver"
    markercolor = "C1"
    px = 1 / rcParams["figure.dpi"]
    fig, ax = plt.subplots(figsize=(1920 * px, 1080 * px), facecolor=bgcolor)
    ax.set(facecolor=bgcolor)
    ax.axis("off")
    ax.invert_yaxis()
    (marker,) = ax.plot(
        xx[:1], yy[:1], color=markercolor, zorder=10, lw=0, marker="o", ms=10
    )
    (there_path,) = ax.plot(xx[:1], yy[:1], "-", color="C8", zorder=5, lw=4, alpha=0.8)
    (back_path,) = ax.plot(xx[:1], yy[:1], "-", color="C1", zorder=5, lw=4, alpha=0.8)
    (again_path,) = ax.plot(xx[:1], yy[:1], "-", color="C3", zorder=5, lw=4, alpha=0.8)
    wind_markers = {}
    for wind_direction in [NORTH, SOUTH, EAST, WEST]:
        (winds_plot,) = ax.plot(
            wind_steps[0][wind_direction][0],
            wind_steps[0][wind_direction][1],
            color=snowcolor,
            lw=0,
            ms=4,
            marker="o",  # PATHCHARS[wind_direction],
            alpha=0.6,
        )
        wind_markers[wind_direction] = winds_plot
    # Show walls
    patches = [
        Rectangle((xmin + 0.5, ymin - 1.5), width, 1, color=wallcolor),
        Rectangle((xmin - 0.5, ymax + 0.5), width - 1, 1, color=wallcolor),
        Rectangle((xmin - 1.5, ymin - 1.5), 1, height + 2, color=wallcolor),
        Rectangle((xmax + 0.5, ymin - 0.5), 1, height + 1, color=wallcolor),
    ]
    ax.add_collection(PatchCollection(patches, match_original=True, zorder=7))
    ax.autoscale_view()
    ax.axis("equal")
    fig.subplots_adjust(left=0.0, right=1.0)

    def animate(i):
        marker.set(
            xdata=xx[i : i + 1],
            ydata=yy[i : i + 1],
        )
        if i <= len(there):
            there_path.set(
                xdata=xx[: i + 1],
                ydata=yy[: i + 1],
            )
        elif i <= len(there) + len(back):
            back_path.set(xdata=xx[len(there) : i + 1], ydata=yy[len(there) : i + 1])
        else:
            again_path.set(
                xdata=xx[len(there) + len(back) : i + 1],
                ydata=yy[len(there) + len(back) : i + 1],
            )
        for wind_direction, winds_plot in wind_markers.items():
            winds_plot.set(
                xdata=wind_steps[i][wind_direction][0],
                ydata=wind_steps[i][wind_direction][1],
            )
        return (
            marker,
            there_path,
            back_path,
            again_path,
            *wind_markers.values(),
        )

    fig.tight_layout()
    ani = animation.FuncAnimation(
        fig, animate, interval=200, blit=True, save_count=len(xx), frames=len(xx)
    )

    # writer = animation.FFMpegWriter(fps=15, metadata=dict(artist="me"), bitrate=1800)
    # ani.save("day_24.mp4", writer=writer)

    plt.show()
