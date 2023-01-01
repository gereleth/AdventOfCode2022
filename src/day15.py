# Day 15: Beacon Exclusion Zone
# Problem statement: https://adventofcode.com/2022/day/15

import re
from util import Segment1D, Segment1DCollection, Segment2D
from collections import namedtuple

day_title = "Beacon Exclusion Zone"


Point = namedtuple("Point", ["x", "y"])

beacon_regex = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)


def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def parse_input(text_input):
    res = []
    for line in text_input.split("\n"):
        sx, sy, bx, by = re.findall(beacon_regex, line)[0]
        sensor = Point(int(sx), int(sy))
        beacon = Point(int(bx), int(by))
        res.append((sensor, beacon))
    return res


def part1(text_input):
    y = 2000000
    # y = 10
    impossible = Segment1DCollection([])
    beacons = set()
    sensors_beacons = parse_input(text_input)
    for sensor, beacon in sensors_beacons:
        if beacon.y == y:
            beacons.add(beacon.x)
        bb = Point(sensor.x, y)
        dist_beacon = manhattan_distance(sensor, beacon)
        dist_bb = manhattan_distance(sensor, bb)
        if dist_bb > dist_beacon:
            continue
        dx = dist_beacon - dist_bb
        impossible += Segment1D(sensor.x - dx, sensor.x + dx)
    return len(impossible) - sum(b in impossible for b in beacons)


def part2(text_input):
    # L = 20
    L = 4000000
    sensors_beacons = parse_input(text_input)

    # rotate the board 45 degrees and use coordinates (d,p) instead of (x,y)
    # d = x + y - L
    # p = x - y
    # Then areas around sensors are squares
    # And the total area is a rhombus instead, having abs(d) + abs(p) <= L

    # We begin from full area and subtract impossible rectangles located around sensors
    # Until only one point remains
    possible = [Segment2D(-L, L, -L, L)]

    # determine if a rectangle still intersects the rhombus
    def rectangle_in_range(r):
        if r.x0 * r.x1 <= 0 or r.y0 * r.y1 <= 0:
            return True
        return any(
            abs(d) + abs(p) <= L
            for (d, p) in (
                (r.x0, r.y0),
                (r.x1, r.y0),
                (r.x0, r.y1),
                (r.x1, r.y1),
            )
        )

    for sensor, beacon in sorted(
        sensors_beacons, key=lambda x: manhattan_distance(x[0], x[1])
    ):
        radius = manhattan_distance(sensor, beacon)
        d0 = sensor.x + sensor.y - L
        p0 = sensor.x - sensor.y
        exclude = Segment2D(d0 - radius, d0 + radius, p0 - radius, p0 + radius)
        possible = [
            res
            for rectangle in possible
            for res in rectangle.difference(exclude)
            if rectangle_in_range(res)
        ]
    rect = possible[0]
    d, p = rect.x0, rect.y0
    x = (L + d + p) // 2
    y = x - p
    return 4000000 * x + y
