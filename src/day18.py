# Day 18: Boiling Boulders
# Problem statement: https://adventofcode.com/2022/day/18

import math
from collections import namedtuple

day_title = "Boiling Boulders"


Point = namedtuple("Point", ["x", "y", "z"])

DELTAS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def get_lava_points_set(text_input):
    res = set()
    for line in text_input.split("\n"):
        res.add(Point(*map(int, line.split(","))))
    return res


def part1(text_input):
    lava = get_lava_points_set(text_input)
    surface_area = 0
    for point in lava:
        for dx, dy, dz in DELTAS:
            neighbour = Point(point.x + dx, point.y + dy, point.z + dz)
            if neighbour not in lava:
                surface_area += 1
    return surface_area


def part2(text_input):
    # flood fill from outside, count lava neighbours
    lava = get_lava_points_set(text_input)
    xmin, ymin, zmin = [math.inf] * 3
    xmax, ymax, zmax = [-math.inf] * 3
    for x, y, z in lava:
        xmin = min(xmin, x - 1)
        xmax = max(xmax, x + 1)
        ymin = min(ymin, y - 1)
        ymax = max(ymax, y + 1)
        zmin = min(zmin, z - 1)
        zmax = max(zmax, z + 1)
    surface_area = 0
    to_check = set((Point(xmin, ymin, zmin),))
    checked = set()
    while len(to_check) > 0:
        point = to_check.pop()
        for dx, dy, dz in DELTAS:
            neighbour = Point(point.x + dx, point.y + dy, point.z + dz)
            if neighbour in lava:
                surface_area += 1
            elif (
                neighbour in checked
                or neighbour.x < xmin
                or neighbour.x > xmax
                or neighbour.y < ymin
                or neighbour.y > ymax
                or neighbour.z < zmin
                or neighbour.z > zmax
            ):
                continue
            else:
                to_check.add(neighbour)
        checked.add(point)
    return surface_area
