# Day 14: Regolith Reservoir
# Problem statement: https://adventofcode.com/2022/day/14

from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PatchCollection
from collections import namedtuple

day_title = "Regolith Reservoir"


Point = namedtuple("Point", ["x", "y"])


class Cave:
    def __init__(self, text_input: str, floor=False):
        self.start = Point(500, 0)
        self.cave = {}
        for segment in text_input.split("\n"):
            points = segment.split(" -> ")
            points = [Point(*map(int, point.split(","))) for point in points]
            for p1, p2 in zip(points[:-1], points[1:]):
                for x in range(min(p1.x, p2.x), max(p1.x + 1, p2.x + 1)):
                    for y in range(min(p1.y, p2.y), max(p1.y + 1, p2.y + 1)):
                        self.cave[Point(x, y)] = "rock"
        self.maxy = max(point.y for point in self.cave.keys())
        self.floor = floor
        self.fall_route = [self.start]

    def drop_sand_grain(self):
        abyss = False
        atrest = False
        if len(self.fall_route) == 0:
            return None
        while not atrest:
            atrest = True
            point = self.fall_route[-1]
            for dx in (0, -1, 1):
                move_option = Point(point.x + dx, point.y + 1)
                if not self.floor and move_option.y > self.maxy:
                    abyss = True
                    break
                if move_option not in self.cave and move_option.y < self.maxy + 2:
                    point = move_option
                    atrest = False
                    self.fall_route.append(point)
                    break
            if abyss:
                return None
        point = self.fall_route.pop()
        self.cave[point] = "sand"
        return point


def part1(text_input):
    cave = Cave(text_input, floor=False)
    sand = 0
    while cave.drop_sand_grain() is not None:
        sand += 1
    return sand


def part2(text_input):
    cave = Cave(text_input, floor=True)
    sand = 0
    while cave.drop_sand_grain() != cave.start:
        sand += 1
    return sand + 1  # +1 because start point isn't counted yet


def visualize(text_input: str):
    # This animation gets really laggy with more sand
    # Because I don't know how to do "add circle and forget about it"
    # So thousands of sand circles are redrawn with each frame
    # The horror
    FW, FH = 12, 8
    fig, ax = plt.subplots(figsize=(FW, FH), facecolor="#444")
    ax.axis("off")

    cave = Cave(text_input, floor=False)
    xmax = max(p.x for p in cave.cave.keys())
    xmin = min(p.x for p in cave.cave.keys())
    ylim = (-1, cave.maxy + 3)
    dx = FW * (ylim[1] - ylim[0]) / FH
    x0 = cave.start[0]
    walls = [
        Rectangle((p.x - 0.5, p.y - 0.5), 1, 1)
        for p, content in cave.cave.items()
        if content == "rock"
    ]
    walls += [Rectangle((x0 - dx * 0.5, cave.maxy + 1.5), dx, 1)]
    ax.add_collection(PatchCollection(walls, fc="brown"))
    ax.set(
        ylim=ylim,
        xlim=(x0 - dx / 2, x0 + dx / 2),
        aspect="equal",
        adjustable="box",
    )
    ax.invert_yaxis()

    (trail,) = ax.plot([], [], "-", color="#cc8", lw=2)
    circles = []

    done = False

    def frames():
        i = 0
        while not done:
            yield i
            i += 1

    def animate(i):
        nonlocal done
        if i == 0:
            return (trail,)
        else:
            todo = max(len(circles) // 100, 1) if cave.floor else 1
            for _ in range(todo):
                point = cave.drop_sand_grain()
                if point is None:
                    cave.floor = True
                elif not done:
                    circle = ax.add_artist(
                        Circle(point, radius=0.5, fc="#996" if cave.floor else "#cc8")
                    )
                    circles.append(circle)
                    done = point == cave.start

            trail.set(
                xdata=[p.x for p in cave.fall_route],
                ydata=[p.y for p in cave.fall_route],
            )

        return (trail, *circles)

    fig.tight_layout()

    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=50,
        blit=True,
        frames=frames,
        # frames=45 * 30,
        repeat=False,
    )

    # writer = animation.FFMpegWriter(fps=24, metadata=dict(artist="me"), bitrate=1800)
    # ani.save("day_14.mp4", writer=writer)

    plt.show()


if __name__ == "__main__":
    folder = Path(__file__).parent.parent
    with open(folder / "inputs" / "day14" / "task.txt") as f:
        content = f.read().rstrip()
    visualize(content)
