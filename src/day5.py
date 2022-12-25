# Day 5: Supply Stacks
# Problem statement: https://adventofcode.com/2022/day/5

from collections import namedtuple

day_title = "Supply Stacks"


def parse_stacks(stacks):
    lines = stacks.split("\n")
    num_stacks = int(lines[-1].split()[-1])
    stacks = [[] for _ in range(num_stacks)]
    for line in reversed(lines[:-1]):
        for i in range(num_stacks):
            crate = line[1 + 4 * i]
            if crate != " ":
                stacks[i].append(crate)
    return stacks


def parse_moves(moves):
    for line in moves.split("\n"):
        num, from_stack, to_stack = map(int, line.split()[1::2])
        yield (num, from_stack - 1, to_stack - 1)


def part1(text_input):
    stacks, moves = text_input.split("\n\n")
    stacks = parse_stacks(stacks)
    for num, from_stack, to_stack in parse_moves(moves):
        for _ in range(num):
            elem = stacks[from_stack].pop()
            stacks[to_stack].append(elem)
    return "".join(stack[-1] for stack in stacks)


def part2(text_input):
    stacks, moves = text_input.split("\n\n")
    stacks = parse_stacks(stacks)
    for num, from_stack, to_stack in parse_moves(moves):
        elems = [stacks[from_stack].pop() for _ in range(num)]
        stacks[to_stack].extend(reversed(elems))
    return "".join(stack[-1] for stack in stacks)
