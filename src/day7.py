# Day 7: No Space Left On Device
# Problem statement: https://adventofcode.com/2022/day/7

from collections import defaultdict

day_title = "No Space Left On Device"


def directory_sizes(text_input: str):
    path = []
    sizes = defaultdict(int)
    for line in text_input.split("\n"):
        line = line.strip()
        # print(line)
        if line.startswith("$ cd"):
            dirname = line[5:]
            if dirname == "..":
                path.pop()
            else:
                path.append(dirname)
        elif line == "$ ls" or line.startswith("dir"):
            pass
        else:
            size, name = line.split()
            size = int(size)
            addto = ""
            for part in path:
                addto = part if addto == "" else addto + "/" + part
                sizes[addto] += size
    return sizes


def part1(text_input: str):
    sizes = directory_sizes(text_input)
    total = sum(size for size in sizes.values() if size <= 100000)
    return total


def part2(text_input):
    sizes = directory_sizes(text_input)
    free = 70_000_000 - sizes["/"]
    need = 30_000_000
    delta = need - free
    todelete = min(size for size in sizes.values() if size >= delta)
    return todelete
