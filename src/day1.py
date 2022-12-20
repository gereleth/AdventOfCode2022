# Day 1: Calorie Counting
# Problem statement: https://adventofcode.com/2022/day/1


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


def run(input_path):
    print("Day 1 : Calorie Counting")
    with open(input_path) as f:
        content = f.read()
    print("Part 1:", part1(content))
    print("Part 2:", part2(content))
