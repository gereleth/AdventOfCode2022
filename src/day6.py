# Day 6: Tuning Trouble
# Problem statement: https://adventofcode.com/2022/day/5


def find_marker(text, nunique=4):
    text = text.strip()
    for i in range(len(text) + 1 - nunique):
        chars = text[i : i + nunique]
        if len(chars) == len(set(chars)):
            return i + nunique
    return -1


def part1(text_input):
    return find_marker(text_input, nunique=4)


def part2(text_input):
    return find_marker(text_input, nunique=14)


def run(input_path):
    print("Day  6: Tuning Trouble")
    with open(input_path) as f:
        content = f.read()
    print("Part 1:", part1(content))
    print("Part 2:", part2(content))
