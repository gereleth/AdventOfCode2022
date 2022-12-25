# Day 1: Calorie Counting
# Problem statement: https://adventofcode.com/2022/day/1

day_title = "Calorie Counting"


def part1(text_input):
    max_calories = 0
    elfs = text_input.strip().split("\n\n")
    for elf in elfs:
        calories = sum(map(int, elf.split()))
        max_calories = max(calories, max_calories)
    return max_calories


def part2(text_input):
    top3 = [0, 0, 0]
    elfs = text_input.strip().split("\n\n")
    for elf in elfs:
        calories = sum(map(int, elf.split()))
        if calories > top3[0]:
            top3.append(calories)
            top3 = sorted(top3)[-3:]
    return sum(top3)
