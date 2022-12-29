# Day 13: Distress Signal
# Problem statement: https://adventofcode.com/2022/day/13

import re
from itertools import zip_longest

day_title = "Distress Signal"

invalid_characters_regex = re.compile(r"[^\d,\[\]\s]")


def check_input(text_input):
    if re.search(invalid_characters_regex, text_input):
        raise ValueError("Invalid characters in input")


def in_right_order(left, right):
    for l, r in zip_longest(left, right):
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return True
            elif l > r:
                return False
        elif l is None:
            return True
        elif r is None:
            return False
        else:
            l = l if isinstance(l, list) else [l]
            r = r if isinstance(r, list) else [r]
            res = in_right_order(l, r)
            if res is not None:
                return res


def part1(text_input):
    check_input(text_input)
    pairs = text_input.split("\n\n")
    total = 0
    for i, pair in enumerate(pairs):
        left, right = pair.split("\n")
        left = eval(left)
        right = eval(right)
        if in_right_order(left, right):
            total += i + 1
    return total


def compare_sort(items):
    if len(items) <= 1:
        return items
    item = items.pop()
    before = []
    after = []
    for other in items:
        if in_right_order(item, other):
            after.append(other)
        else:
            before.append(other)
    return compare_sort(before) + [item] + compare_sort(after)


def part2(text_input):
    check_input(text_input)
    items = [eval(item) for item in text_input.replace("\n\n", "\n").split("\n")] + [
        [[2]],
        [[6]],
    ]
    sorted_items = compare_sort(items)
    i1, i2, *_ = [
        i + 1 for i, item in enumerate(sorted_items) if str(item) in ("[[2]]", "[[6]]")
    ]
    return i1 * i2
