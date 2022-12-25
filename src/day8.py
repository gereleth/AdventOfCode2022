# Day 8: Treetop Tree House
# Problem statement: https://adventofcode.com/2022/day/8

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import splprep, splev

day_title = "Treetop Tree House"


def parse_heights(text_input: str):
    heights = [[int(char) for char in line] for line in text_input.split("\n")]
    return heights


def part1(text_input: str):
    trees = parse_heights(text_input)
    visible = [[0 for i in row] for row in trees]
    for row in range(len(trees)):
        maxheight = -1
        for i, tree in enumerate(trees[row]):
            if tree > maxheight:
                visible[row][i] = 1
                maxheight = tree
        maxheight = -1
        for i, tree in enumerate(reversed(trees[row])):
            if tree > maxheight:
                visible[row][-1 - i] = 1
                maxheight = tree
    for col in range(len(trees[0])):
        maxheight = -1
        for row in range(len(trees)):
            tree = trees[row][col]
            if tree > maxheight:
                visible[row][col] = 1
                maxheight = tree
        maxheight = -1
        for row in range(len(trees)):
            tree = trees[-1 - row][col]
            if tree > maxheight:
                visible[-1 - row][col] = 1
                maxheight = tree
    return sum(sum(v) for v in visible)


def part2(text_input):
    trees = parse_heights(text_input)
    best = 0
    for row in range(1, len(trees) - 1):
        for col in range(1, len(trees[0]) - 1):
            tree = trees[row][col]
            up = 0
            for uprow in range(row, 0, -1):
                up += 1
                if trees[uprow - 1][col] >= tree:
                    break
            down = 0
            for uprow in range(row, len(trees) - 1, 1):
                down += 1
                if trees[uprow + 1][col] >= tree:
                    break
            left = 0
            for lcol in range(col, 0, -1):
                left += 1
                if trees[row][lcol - 1] >= tree:
                    break
            right = 0
            for lcol in range(col, len(trees[0]) - 1, 1):
                right += 1
                if trees[row][lcol + 1] >= tree:
                    break
            score = up * down * left * right
            if score > best:
                best = score
    return best


def visualize(text_input: str, crop_size=0):
    trees = parse_heights(text_input)
    # limit size so that animation doesn't last forever
    if crop_size > 0:
        trees = [list(row[:crop_size]) for row in trees[:crop_size]]
    H = len(trees)
    W = len(trees[0])
    best = 0
    scan_color = "C1"
    best_color = "gold"
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
    image = ax.imshow(trees, cmap="Greens_r", vmin=-1, vmax=10)
    # fig.colorbar(image, ax=ax, label="Tree height", location="bottom")
    (tree_marker,) = ax.plot([1], [1], "o", ms=12, color=scan_color)
    (view_area,) = ax.plot([1], [1], "-", color=scan_color, lw=2)
    (horiz_scores,) = ax.plot([1, 1], [1, 1], "-", color=scan_color, lw=2)
    (vert_scores,) = ax.plot([1, 1], [1, 1], "-", color=scan_color, lw=2)
    # (best_tree_marker,) = ax.plot([2], [2], "s", ms=24, color=best_color)
    (best_horiz_scores,) = ax.plot([1, 1], [1, 1], "-", color=best_color, lw=4)
    (best_vert_scores,) = ax.plot([1, 1], [1, 1], "-", color=best_color, lw=4)
    (best_view_area,) = ax.plot([1], [1], "-", color=best_color, lw=4)
    ax.axis("off")

    best = 0

    def animate(i):
        nonlocal best
        col = 1 + i % (W - 2)
        row = 1 + i // (W - 2)
        tree = trees[row][col]
        up = 0
        for uprow in range(row, 0, -1):
            up += 1
            if trees[uprow - 1][col] >= tree:
                break
        down = 0
        for uprow in range(row, len(trees) - 1, 1):
            down += 1
            if trees[uprow + 1][col] >= tree:
                break
        left = 0
        for lcol in range(col, 0, -1):
            left += 1
            if trees[row][lcol - 1] >= tree:
                break
        right = 0
        for lcol in range(col, len(trees[0]) - 1, 1):
            right += 1
            if trees[row][lcol + 1] >= tree:
                break
        score = up * down * left * right
        tree_marker.set(xdata=[col], ydata=[row])
        horiz_scores.set(xdata=[col - left, col + right], ydata=[row, row])
        vert_scores.set(xdata=[col, col], ydata=[row - up, row + down])

        # splines recipe from here
        # https://stackoverflow.com/questions/69247073/how-to-smooth-line-between-polygon-points
        x = [col + right, col, col - left, col, col + right]
        y = [row, row + down, row, row - up, row]
        tck, _ = splprep([x, y], s=0, per=True)
        xx, yy = splev(np.linspace(0, 1, 100), tck, der=0)
        view_area.set(xdata=xx, ydata=yy)
        # print(f"i={i} x={col} y={row} up={up} down={down} left={left} right={right}")
        if score > best:
            best = score
            # best_tree_marker.set(xdata=[col], ydata=[row])
            best_horiz_scores.set(xdata=[col - left, col + right], ydata=[row, row])
            best_vert_scores.set(xdata=[col, col], ydata=[row - up, row + down])
            best_view_area.set(xdata=xx, ydata=yy)
        return (
            tree_marker,
            horiz_scores,
            vert_scores,
            view_area,
            # best_tree_marker,
            best_horiz_scores,
            best_vert_scores,
            best_view_area,
        )

    frames = (W - 2) * (H - 2)
    ani = animation.FuncAnimation(fig, animate, interval=100, blit=True, frames=frames)

    # writer = animation.FFMpegWriter(fps=10, metadata=dict(artist="me"), bitrate=1800)
    # ani.save("day_8.mp4", writer=writer)

    plt.show()


if __name__ == "__main__":
    with open("inputs/day8/task.txt") as f:
        content = f.read()
    visualize(content.rstrip(), crop_size=20)
