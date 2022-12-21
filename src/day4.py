# Day 4: Camp Cleanup
# Problem statement: https://adventofcode.com/2022/day/4


def part1(text_input):
    total = 0
    for line in text_input.split("\n"):
        aa, bb = line.split(",")
        a1, a2 = map(int, aa.split("-"))
        b1, b2 = map(int, bb.split("-"))
        if (a1 <= b1 and a2 >= b2) or (b1 <= a1 and b2 >= a2):
            total += 1
    return total


def part2(text_input):
    total = 0
    for line in text_input.split("\n"):
        aa, bb = line.split(",")
        a1, a2 = map(int, aa.split("-"))
        b1, b2 = map(int, bb.split("-"))
        (x1, x2), (y1, y2) = sorted([(a1, a2), (b1, b2)])
        # x1 ------- x2
        #       y1 --------y2               ✅
        #                  y1 ------- y2    ❌
        if x2 >= y1:
            total += 1
    return total


def run(input_path):
    print("Day  4: Camp Cleanup")
    with open(input_path) as f:
        content = f.read()
    print("Part 1:", part1(content))
    print("Part 2:", part2(content))
