# Day 9: Rope Bridge
# Problem statement: https://adventofcode.com/2022/day/9

from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import math

day_title = "Rope Bridge"

DELTAS = {
    # (dy, dx)
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "U": (-1, 0),
}


def move_tail(head, tail):
    headx, heady = head
    tailx, taily = tail
    dx = headx - tailx
    dy = heady - taily
    if (abs(dx) + abs(dy) <= 1) or (abs(dx) == 1 and abs(dy) == 1):
        pass
    else:
        tailx += 0 if dx == 0 else 1 if dx > 0 else -1
        taily += 0 if dy == 0 else 1 if dy > 0 else -1
    return tailx, taily


def move_snake(snake, direction):
    dy, dx = DELTAS[direction]
    headx, heady = snake[0]
    snake[0] = (headx + dx, heady + dy)
    for part in range(1, len(snake)):
        snake[part] = move_tail(snake[part - 1], snake[part])


def moves_iter(text_input):
    for line in text_input.split("\n"):
        direction, steps = line.split()
        for _ in range(int(steps)):
            yield direction


def part1(text_input):
    visited = set([(0, 0)])
    LENGTH = 2
    snake = [(0, 0) for _ in range(LENGTH)]
    for direction in moves_iter(text_input):
        move_snake(snake, direction)
        visited.add(snake[-1])
    return len(visited)


def part2(text_input):
    visited = set([(0, 0)])
    LENGTH = 10
    snake = [(0, 0) for _ in range(LENGTH)]
    for direction in moves_iter(text_input):
        move_snake(snake, direction)
        visited.add(snake[-1])
    return len(visited)


def visualize(text_input: str, speedup_every=0):
    visited_1 = set([(0, 0)])
    visited_2 = set([(0, 0)])
    snake_1 = [(0, 0) for _ in range(2)]
    snake_2 = [(0, 0) for _ in range(10)]
    moves = list(moves_iter(text_input))

    M = len(moves) + 1

    if speedup_every > 0:
        chunks = math.ceil(-0.5 + math.sqrt((2 * M / speedup_every - 0.25))) + 1
        frames = chunks * speedup_every
    else:
        frames = M

    fig, (ax1, ax2) = plt.subplots(
        nrows=1, ncols=2, figsize=(12, 6), facecolor="silver"
    )
    for ax in (ax1, ax2):
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_facecolor("white")
    fig.subplots_adjust(top=0.95, bottom=0.02, left=0.02, right=0.98, wspace=0.02)

    xmin, xmax, ymin, ymax = -3, 3, -3, 3

    (trail_1,) = ax1.plot([0], [0], ".", ms=4, color="#aec7e8")
    (trail_2,) = ax2.plot([0], [0], ".", ms=4, color="#ffbb78")
    (p_snake_1,) = ax1.plot([0], [0], "-o", color="C0", lw=5, alpha=0.9)
    (p_snake_2,) = ax2.plot([0], [0], "-o", color="C1", lw=5, alpha=0.9)
    title_1 = ax1.set_title("Visited: 0")
    title_2 = ax2.set_title("Visited: 0")

    move_index = 0

    def animate(i):
        nonlocal xmin, xmax, ymin, ymax
        nonlocal visited_1, visited_2, snake_1, snake_2, move_index
        if i == 0:
            visited_1 = set([(0, 0)])
            visited_2 = set([(0, 0)])
            snake_1 = [(0, 0) for _ in range(2)]
            snake_2 = [(0, 0) for _ in range(10)]
            move_index = 0
            xmin, xmax, ymin, ymax = -3, 3, -3, 3
        else:
            if speedup_every > 0:
                take_moves = 1 + (i + 1) // speedup_every
            else:
                take_moves = 1
            for _ in range(take_moves):
                if move_index >= len(moves):
                    continue
                direction = moves[move_index]
                move_index += 1
                move_snake(snake_1, direction)
                move_snake(snake_2, direction)
                xmin = min(xmin, *(v[0] for v in snake_1), *(v[0] for v in snake_2))
                xmax = max(xmax, *(v[0] for v in snake_1), *(v[0] for v in snake_2))
                ymin = min(ymin, *(v[1] for v in snake_1), *(v[1] for v in snake_2))
                ymax = max(ymax, *(v[1] for v in snake_1), *(v[1] for v in snake_2))
                visited_1.add(snake_1[-1])
                visited_2.add(snake_2[-1])

        trail_1.set(xdata=[v[0] for v in visited_1], ydata=[v[1] for v in visited_1])
        trail_2.set(xdata=[v[0] for v in visited_2], ydata=[v[1] for v in visited_2])
        p_snake_1.set(xdata=[v[0] for v in snake_1], ydata=[v[1] for v in snake_1])
        p_snake_2.set(xdata=[v[0] for v in snake_2], ydata=[v[1] for v in snake_2])

        dx, dy = xmax - xmin, ymax - ymin
        x0, y0 = (xmax + xmin) * 0.5, (ymax + ymin) * 0.5
        dl = max(dx, dy) / 2
        for ax in (ax1, ax2):
            ax.set(
                xlim=(x0 - 1.05 * dl, x0 + 1.05 * dl),
                ylim=(y0 + 1.05 * dl, y0 - 1.05 * dl),
            )
        title_1.set_text(f"Visited: {len(visited_1)}")
        title_2.set_text(f"Visited: {len(visited_2)}")
        return (trail_1, trail_2, p_snake_1, p_snake_2, title_1, title_2)

    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=50,
        blit=False,
        frames=frames,
        repeat_delay=3000,
    )

    # writer = animation.FFMpegWriter(fps=24, metadata=dict(artist="me"), bitrate=1800)
    # ani.save("day_9.mp4", writer=writer)

    plt.show()


if __name__ == "__main__":
    folder = Path(__file__).parent.parent
    with open(folder / "inputs" / "day9" / "task.txt") as f:
        content = f.read().rstrip()
    visualize(content, speedup_every=24)
