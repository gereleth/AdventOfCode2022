# Day 3: Rucksack Reorganization
# Problem statement: https://adventofcode.com/2022/day/3

day_title = "Rucksack Reorganization"


def symbol_score(symbol):
    # ord('a') to ord('z') is 97 to 122
    # ord('A') to ord('Z') is 65 to 90
    delta = 96 if symbol.islower() else 38
    s = ord(symbol) - delta
    return s


def part1(text_input):
    total = 0
    for line in text_input.split():
        half_point = len(line) // 2
        first_half = set(line[:half_point])
        second_half = set(line[half_point:])
        common_symbol = next(iter(first_half.intersection(second_half)))
        total += symbol_score(common_symbol)
    return total


def part2(text_input):
    total = 0
    group = []
    for line in text_input.split():
        group.append(set(line))
        if len(group) == 3:
            common = group[0].intersection(group[1]).intersection(group[2])
            symbol = next(iter(common))
            total += symbol_score(symbol)
            group = []
    return total
