# Day 16: Proboscidea Volcanium
# Problem statement: https://adventofcode.com/2022/day/16

import re
import networkx as nx
import heapq
from collections import namedtuple


day_title = "Proboscidea Volcanium"


Valve = namedtuple("Valve", ["label", "flow_rate", "tunnels"])
ExplorerState = namedtuple("ExplorerState", ["id", "turns", "position"])
State = namedtuple("State", ["pressure", "explorers", "closed_valves"])

valve_regex = re.compile(
    r"Valve (\S+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
)


class Cave:
    def __init__(self, text_input: str, turns: int, n_explorers=1):
        self.valves = self.parse_valves(text_input)
        self.turns = turns
        self.n_explorers = n_explorers
        self.nonzero_valves = set(
            label for label, v in self.valves.items() if v.flow_rate > 0
        )
        graph = nx.Graph()
        graph.add_edges_from(
            [
                (valve.label, tunnel)
                for valve in self.valves.values()
                for tunnel in valve.tunnels
            ]
        )
        self.distances = dict(nx.all_pairs_shortest_path_length(graph))
        self.seen = set()  # cache of seen states to avoid repeats

    def parse_valves(self, text_input: str):
        valves = {}
        for line in text_input.split("\n"):
            label, flow, tunnels = re.findall(valve_regex, line)[0]
            valves[label] = Valve(label, int(flow), tuple(tunnels.split(", ")))
        return valves

    def initial_state(self):
        return State(
            pressure=0,
            explorers=tuple(
                ExplorerState(id=i, turns=self.turns, position="AA")
                for i in range(self.n_explorers)
            ),
            closed_valves=tuple(self.nonzero_valves),
        )

    def upper_bound(self, state: State) -> int:
        """Upper bound of pressure achievable from current state

        If we could send out shadow clones to all closed valves simultaneously
        Then we'd get this much pressure =)
        """
        pressure = state.pressure
        for label in state.closed_valves:
            flow = self.valves[label].flow_rate
            could_gain = 0
            for explorer in state.explorers:
                distance = self.distances[explorer.position][label]
                gain = (explorer.turns - distance - 1) * flow
                could_gain = max(could_gain, gain)
            pressure += could_gain
        return pressure

    def explore_next_states(self, state: State):
        """Generate next states depending on which valve to open next"""
        # select whoever has the most turns left
        explorer = max(state.explorers, key=lambda x: x.turns)
        if explorer.turns <= 1:
            # no time to do anything else from here
            return []
        states = []
        # they could try and open one of the currently closed valves
        for label in state.closed_valves:
            flow = self.valves[label].flow_rate
            distance = self.distances[explorer.position][label]
            gain = (explorer.turns - distance - 1) * flow
            if gain <= 0:
                continue
            states.append(
                State(
                    pressure=state.pressure + gain,
                    explorers=tuple(
                        (
                            e
                            if e != explorer
                            else ExplorerState(
                                id=explorer.id,
                                turns=explorer.turns - distance - 1,
                                position=label,
                            )
                            for e in state.explorers
                        )
                    ),
                    closed_valves=tuple(v for v in state.closed_valves if v != label),
                )
            )
        # or they could do nothing at all
        # and let the other explorers handle things
        if len(state.explorers) > 0:
            states.append(
                State(
                    pressure=state.pressure,
                    explorers=tuple(
                        (
                            e
                            if e != explorer
                            else ExplorerState(
                                id=explorer.id, turns=0, position=explorer.position
                            )
                            for e in state.explorers
                        )
                    ),
                    closed_valves=state.closed_valves,
                )
            )
        return states

    def have_seen_this_state(self, state):
        gist = tuple(
            (state.pressure, *sorted((e.turns, e.position) for e in state.explorers))
        )
        if gist in self.seen:
            return True
        self.seen.add(gist)
        return False

    def best_pressure(self):
        state = self.initial_state()
        ub = self.upper_bound(state)
        queue = [(-ub, state)]
        best = 0
        heapq.heapify(queue)
        i = 1
        while len(queue) > 0:
            neg_ub, prev_state = heapq.heappop(queue)
            if -neg_ub <= best:
                continue
            for state in self.explore_next_states(prev_state):
                if state.pressure > best:
                    best = state.pressure
                ub = self.upper_bound(state)
                if ub <= best:
                    continue
                if self.have_seen_this_state(state):
                    continue
                heapq.heappush(queue, (-ub, state))
                # i += 1
                # if i % 1000 == 0:
                #     print(
                #         f"iter {i}\tbest {best}\tub {-neg_ub}\tqueue {len(queue)}"
                #     )
        return best


def part1(text_input):
    cave = Cave(text_input, turns=30, n_explorers=1)
    best = cave.best_pressure()
    return best


def part2(text_input):
    cave = Cave(text_input, turns=26, n_explorers=2)
    best = cave.best_pressure()
    return best
