# Day 10: Cathode-Ray Tube
# Problem statement: https://adventofcode.com/2022/day/10

from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib import transforms
import numpy as np

day_title = "Cathode-Ray Tube"


def command_iter(text_input: str):
    for line in text_input.split("\n"):
        command, *args = line.split()
        if command == "noop":
            yield command, None
        else:
            yield command, int(args[0])


def get_x_values(text_input: str):
    x = []
    current = 1
    for command, arg in command_iter(text_input):
        if command == "noop":
            x.append(current)
        elif command == "addx":
            x.extend((current, current))
            current += arg
    return x


def part1(text_input):
    x = get_x_values(text_input)
    total = 0
    for i in range(20, 260, 40):
        total += x[i - 1] * i
    return total


def part2(text_input):
    x = get_x_values(text_input)
    lines = []
    W, H = 40, 6
    for h in range(H):
        row = ""
        for w in range(W):
            index = h * W + w
            if abs(x[index] - w) <= 1:
                row += "▉"
            else:
                row += " "
        lines.append(row)
    return "\n" + "\n".join(lines)


def visualize(text_input: str):
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="#444")
    ax.axis("off")
    W, H = 40, 6
    image = np.zeros((H, W), dtype=bool)
    scanner_linewidth = 4

    im = ax.imshow(image, interpolation="none", vmin=-0.3, vmax=1.3, cmap="Greys_r")
    scanner = Rectangle(
        (0, 0),
        width=1,
        height=1,
        facecolor="none",
        edgecolor="#0f0",
        lw=scanner_linewidth,
    )
    sprite = Rectangle((1, 0), width=3, height=H, facecolor="#0f0", alpha=0.4)
    # set scanner and sprite positions half a cell back
    # so they are shown over the correct "screen pixel"
    scanner.set_transform(transforms.Affine2D().translate(-0.5, -0.5) + ax.transData)
    sprite.set_transform(transforms.Affine2D().translate(-1.5, -0.5) + ax.transData)

    ax.add_artist(scanner)
    ax.add_artist(sprite)
    ax.set(xlim=(-1, W), ylim=(H, -1))
    fig.subplots_adjust(left=0, right=1)

    X = get_x_values(text_input)

    def animate(i):
        nonlocal image
        if i == 0:
            image = np.zeros((H, W), dtype=bool)
            scanner.set_xy((0, 0))
            sprite.set_xy((1, 0))
        elif i <= len(X):
            x = X[i - 1]
            w, h = (i - 1) % W, (i - 1) // W
            scanner.set_xy((w, h))
            sprite.set_xy((x, 0))
            if abs(x - w) <= 1:
                image[h, w] = True
            im.set_array(image)

        return (im, sprite, scanner)

    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=100,
        blit=False,
        frames=len(X) + 20,
        # repeat_delay=3000,
    )

    # writer = animation.FFMpegWriter(fps=10, metadata=dict(artist="me"), bitrate=1800)
    # ani.save("day_10.mp4", writer=writer)

    plt.show()


if __name__ == "__main__":
    folder = Path(__file__).parent.parent
    with open(folder / "inputs" / "day10" / "task.txt") as f:
        content = f.read().rstrip()
    visualize(content)
