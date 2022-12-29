# Day 14: Beacon Exclusion Zone
# Problem statement: https://adventofcode.com/2022/day/15

import re
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
    impossible = set()
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
        for d in range(dist_bb - dist_beacon, dist_beacon - dist_bb + 1):
            impossible.add(sensor.x + d)
    return len(impossible - beacons)


def subtract_range(before, subtract):
    # inclusive ranges [from, to]
    # returns list of ranges
    if before[1] < subtract[0] or before[0] > subtract[1]:
        return [before]
    new = []
    if before[0] < subtract[0]:
        new.append((before[0], subtract[0] - 1))
    if subtract[1] < before[1]:
        new.append((subtract[1] + 1, before[1]))
    return new


def part2(text_input):
    # blim, ulim = 0, 20
    blim, ulim = 0, 4000000
    sensors_beacons = parse_input(text_input)
    possible = {x: [(blim, ulim)] for x in range(blim, ulim + 1)}
    for sensor, beacon in sorted(
        sensors_beacons, key=lambda x: -manhattan_distance(x[0], x[1])
    ):
        dist_beacon = manhattan_distance(sensor, beacon)
        for dx in range(-dist_beacon, dist_beacon + 1):
            x = sensor.x + dx
            if x < blim or x > ulim or x not in possible:
                continue
            y0 = max(blim, sensor.y - (dist_beacon - abs(dx)))
            y1 = min(ulim, sensor.y + dist_beacon - abs(dx))
            poss = possible.pop(x)
            newposs = []
            for part in poss:
                for res in subtract_range(part, (y0, y1)):
                    newposs.append(res)
            if len(newposs) > 0:
                possible[x] = newposs
    x, yy = possible.popitem()
    y = yy[0][0]
    return 4000000 * x + y
