# Day 21: Monkey Math
# Problem statement: https://adventofcode.com/2022/day/21

from sympy import Symbol, solveset


def parse_input(text_input):
    values = {}
    calcs = {}
    for line in text_input.split("\n"):
        monkey, operation = line.split(": ")
        if operation.isnumeric():
            values[monkey] = int(operation)
        else:
            operation = tuple(operation.split())
            calcs[monkey] = operation
    return values, calcs


def compute(num1, operation, num2):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        return num1 / num2


def yell_fn(values, calcs):
    def yell(monkey):
        if monkey in values:
            return values[monkey]
        in1, operation, in2 = calcs[monkey]
        num1 = yell(in1)
        num2 = yell(in2)
        return compute(num1, operation, num2)

    return yell


def part1(text_input):
    values, calcs = parse_input(text_input)
    yell = yell_fn(values, calcs)
    result = int(yell("root"))
    return result


def part2(text_input):
    values, calcs = parse_input(text_input)

    values["humn"] = Symbol("x")
    r1, _, r2 = calcs.pop("root")
    calcs["root"] = (r1, "-", r2)

    yell = yell_fn(values, calcs)

    equation = yell("root")
    result = next(iter(solveset(equation)))
    return int(result)


def run(input_path):
    print("Day 21: Monkey Math")
    with open(input_path) as f:
        content = f.read()
    print("Part 1:", part1(content))
    print("Part 2:", part2(content))
