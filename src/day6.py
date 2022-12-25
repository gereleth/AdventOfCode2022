# Day 6: Tuning Trouble
# Problem statement: https://adventofcode.com/2022/day/5

day_title = "Tuning Trouble"


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
