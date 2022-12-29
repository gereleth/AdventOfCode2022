# Day 19: Not Enough Minerals
# Problem statement: https://adventofcode.com/2022/day/19

import math
from collections import namedtuple
import heapq
import re

day_title = "Not Enough Minerals"

BLUEPRINT_REGEX = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
)
blueprint_fields = [
    "id",
    "ore_robot_cost",
    "clay_robot_cost",
    "obsidian_robot_cost_ore",
    "obsidian_robot_cost_clay",
    "geode_robot_cost_ore",
    "geode_robot_cost_obsidian",
]
Blueprint = namedtuple("Blueprint", blueprint_fields)
FactoryState = namedtuple(
    "FactoryState",
    [
        "turns",
        "ore",
        "ore_robots",
        "clay",
        "clay_robots",
        "obsidian",
        "obsidian_robots",
        "geodes",
    ],
)


def parse_blueprint(line: str):
    numbers = re.findall(BLUEPRINT_REGEX, line)[0]
    return Blueprint(
        **{field: int(value) for field, value in zip(blueprint_fields, numbers)}
    )


class Factory:
    def __init__(self, blueprint: Blueprint, max_turns: int):
        self.blueprint = blueprint
        self.max_turns = max_turns
        self.max_ore_need = max(
            blueprint.ore_robot_cost,
            blueprint.clay_robot_cost,
            blueprint.obsidian_robot_cost_ore,
            blueprint.geode_robot_cost_ore,
        )
        self.max_clay_need = blueprint.obsidian_robot_cost_clay
        self.max_obsidian_need = blueprint.geode_robot_cost_obsidian

    def initial_state(self):
        return FactoryState(self.max_turns, 0, 1, 0, 0, 0, 0, 0)

    def geodes_upper_bound(self, state: FactoryState):
        """Can make no more than this many geodes from this state.

        Suppose resources are not consumed when building robots.
        So we only have to save up enough resources for the first build of every robot kind.
        """
        ore = state.ore
        clay = state.clay
        obsi = state.obsidian
        r_ore = state.ore_robots
        r_clay = state.clay_robots
        r_obsi = state.obsidian_robots
        turns = state.turns
        while turns > 0:
            turns -= 1
            ore += r_ore
            clay += r_clay
            obsi += r_obsi
            if r_clay == 0 and ore < self.blueprint.clay_robot_cost:
                r_ore += 1
            elif r_clay == 0 or clay < self.blueprint.obsidian_robot_cost_clay:
                r_clay += 1
            elif r_obsi == 0 or obsi < self.blueprint.geode_robot_cost_obsidian:
                r_obsi += 1
            else:
                return state.geodes + sum(i + 1 for i in range(turns))
        return state.geodes

    def explore_next_crafts(self, state: FactoryState):
        if state.ore_robots < self.max_ore_need:
            # try building an ore mining robot
            need = self.blueprint.ore_robot_cost
            delta = max(0, need - state.ore)
            wait = math.ceil(delta / state.ore_robots) + 1
            if state.turns - wait > 0:
                yield (
                    "ore",
                    FactoryState(
                        turns=state.turns - wait,
                        ore=state.ore + state.ore_robots * wait - need,
                        ore_robots=state.ore_robots + 1,
                        clay=state.clay + state.clay_robots * wait,
                        clay_robots=state.clay_robots,
                        obsidian=state.obsidian + state.obsidian_robots * wait,
                        obsidian_robots=state.obsidian_robots,
                        geodes=state.geodes,
                    ),
                )
        if state.clay_robots < self.max_clay_need:
            # try building a clay robot
            need = self.blueprint.clay_robot_cost
            delta = max(0, need - state.ore)
            wait = math.ceil(delta / state.ore_robots) + 1
            if state.turns - wait > 0:
                yield (
                    "clay",
                    FactoryState(
                        turns=state.turns - wait,
                        ore=state.ore + state.ore_robots * wait - need,
                        ore_robots=state.ore_robots,
                        clay=state.clay + state.clay_robots * wait,
                        clay_robots=state.clay_robots + 1,
                        obsidian=state.obsidian + state.obsidian_robots * wait,
                        obsidian_robots=state.obsidian_robots,
                        geodes=state.geodes,
                    ),
                )
        if state.obsidian_robots < self.max_obsidian_need and state.clay_robots > 0:
            # try building an obsidian robot
            need_ore = self.blueprint.obsidian_robot_cost_ore
            delta_ore = max(0, need_ore - state.ore)
            need_clay = self.blueprint.obsidian_robot_cost_clay
            delta_clay = max(0, need_clay - state.clay)
            wait = (
                max(
                    math.ceil(delta_ore / state.ore_robots),
                    math.ceil(delta_clay / state.clay_robots),
                )
                + 1
            )
            if state.turns - wait > 0:
                yield (
                    "obsidian",
                    FactoryState(
                        turns=state.turns - wait,
                        ore=state.ore + state.ore_robots * wait - need_ore,
                        ore_robots=state.ore_robots,
                        clay=state.clay + state.clay_robots * wait - need_clay,
                        clay_robots=state.clay_robots,
                        obsidian=state.obsidian + state.obsidian_robots * wait,
                        obsidian_robots=state.obsidian_robots + 1,
                        geodes=state.geodes,
                    ),
                )
        if state.obsidian_robots > 0:
            # try building a geode robot
            need_ore = self.blueprint.geode_robot_cost_ore
            delta_ore = max(0, need_ore - state.ore)
            need_obsidian = self.blueprint.geode_robot_cost_obsidian
            delta_obsidian = max(0, need_obsidian - state.obsidian)
            wait = (
                max(
                    math.ceil(delta_ore / state.ore_robots),
                    math.ceil(delta_obsidian / state.obsidian_robots),
                )
                + 1
            )
            if state.turns - wait > 0:
                yield (
                    "geode",
                    FactoryState(
                        turns=state.turns - wait,
                        ore=state.ore + state.ore_robots * wait - need_ore,
                        ore_robots=state.ore_robots,
                        clay=state.clay + state.clay_robots * wait,
                        clay_robots=state.clay_robots,
                        obsidian=state.obsidian
                        + state.obsidian_robots * wait
                        - need_obsidian,
                        obsidian_robots=state.obsidian_robots,
                        geodes=state.geodes + state.turns - wait,
                    ),
                )


def most_geodes(blueprint: Blueprint, turns: int):
    factory = Factory(blueprint, turns)
    start = factory.initial_state()
    queue = [(0, 0, 0, start, "")]
    heapq.heapify(queue)
    best_geodes = 0
    best_crafts = ""
    iteration = 0
    while len(queue) > 0:
        _, _, _, state, previous_crafts = heapq.heappop(queue)
        for craft, next_state in factory.explore_next_crafts(state):
            geodes = next_state.geodes
            if geodes > best_geodes:
                best_geodes = geodes
                best_crafts = previous_crafts + " " + craft
            upper_bound = factory.geodes_upper_bound(next_state)
            if upper_bound <= best_geodes:
                continue
            heapq.heappush(
                queue,
                (
                    -upper_bound,
                    -geodes,
                    iteration,
                    next_state,
                    previous_crafts + " " + craft,
                ),
            )
    return best_geodes, best_crafts


def part1(text_input: str):
    total = 0
    for line in text_input.split("\n"):
        blueprint = parse_blueprint(line)
        best_geodes, _ = most_geodes(blueprint, 24)
        total += best_geodes * blueprint.id
    return total


def part2(text_input):
    total = 1
    for line in text_input.split("\n")[:3]:
        blueprint = parse_blueprint(line)
        best_geodes, _ = most_geodes(blueprint, 32)
        total *= best_geodes
    return total
