# Day 11: Monkey in the Middle
# Problem statement: https://adventofcode.com/2022/day/11

from collections import namedtuple
import re
from operator import mul, add

day_title = "Monkey in the Middle"

Monkey = namedtuple("Monkey", ["id", "items", "operation", "test", "iftrue", "iffalse"])

OPERATIONS = {"*": mul, "+": add}


def parse_monkeys(text_input: str):
    monkeys = []
    for monkey in text_input.split("\n\n"):
        lines = monkey.split("\n")
        num1, op, num2 = lines[2].split("new = ")[1].split()
        if num1 != "old":
            num1 = int(num1)
        if num2 != "old":
            num2 = int(num2)
        op = OPERATIONS[op]
        monkeys.append(
            Monkey(
                id=int(re.findall(r"(\d+)", lines[0])[0]),
                items=list(map(int, re.findall(r"(\d+)", lines[1]))),
                operation=[num1, op, num2],
                test=int(lines[3].split()[-1]),
                iftrue=int(lines[4].split()[-1]),
                iffalse=int(lines[5].split()[-1]),
            )
        )
    return monkeys


def inspect(monkey: Monkey, item: int):
    num1, op, num2 = monkey.operation
    if num1 == "old":
        num1 = item
    if num2 == "old":
        num2 = item
    return op(num1, num2)


def part1(text_input):
    monkeys = parse_monkeys(text_input)
    inspections = [0] * len(monkeys)
    for r in range(20):
        for monkey in monkeys:
            for item in monkey.items:
                inspections[monkey.id] += 1
                new_value = inspect(monkey, item) // 3
                if new_value % monkey.test == 0:
                    monkeys[monkey.iftrue].items.append(new_value)
                else:
                    monkeys[monkey.iffalse].items.append(new_value)
            monkey.items.clear()
    inspections = sorted(inspections, reverse=True)
    return inspections[0] * inspections[1]


def part2(text_input):
    monkeys = parse_monkeys(text_input)
    inspections = [0] * len(monkeys)
    divide_by = 1
    for monkey in monkeys:
        divide_by *= monkey.test
    for r in range(10000):
        for monkey in monkeys:
            for item in monkey.items:
                inspections[monkey.id] += 1
                new_value = inspect(monkey, item) % divide_by
                if new_value % monkey.test == 0:
                    monkeys[monkey.iftrue].items.append(new_value)
                else:
                    monkeys[monkey.iffalse].items.append(new_value)
            monkey.items.clear()
    inspections = sorted(inspections, reverse=True)
    return inspections[0] * inspections[1]
