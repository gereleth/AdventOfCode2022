# Day 20: Grove Positioning System
# Problem statement: https://adventofcode.com/2022/day/20


def mix(ls):
    moved = 0
    move_position = 0
    factor = len(ls) - 1
    while moved < len(ls):
        elem, index = ls[move_position]
        while index != moved:
            move_position = (move_position + 1) % len(ls)
            elem, index = ls[move_position]
        if elem < 0:
            elem = elem % factor
        new_position = (move_position + elem) % factor
        if new_position == 0:
            new_position = factor
        move = ls.pop(move_position)
        ls.insert(new_position, move)
        if new_position <= move_position:
            move_position = (move_position + 1) % len(ls)
        moved += 1
    return ls


def get_answer(ls):
    index = ls.index(0)
    total = 0
    for i in [1000, 2000, 3000]:
        total += ls[(index + i) % len(ls)]
    return total


def part1(text_input):
    ls = [(int(val), index) for index, val in enumerate(text_input.split())]
    ls = mix(ls)
    ls = [m[0] for m in ls]
    return get_answer(ls)


def part2(text_input):
    key = 811589153
    ls = [(int(val) * key, index) for index, val in enumerate(text_input.split())]
    for _ in range(10):
        ls = mix(ls)
    ls = [m[0] for m in ls]
    return get_answer(ls)


def run(input_path):
    print("Day 20: Grove Positioning System")
    with open(input_path) as f:
        content = f.read()
    print("Part 1:", part1(content))
    print("Part 2:", part2(content))
