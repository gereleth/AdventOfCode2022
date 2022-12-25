# Day 2: Rock Paper Scissors
# Problem statement: https://adventofcode.com/2022/day/2

day_title = "Rock Paper Scissors"

R = "rock"
P = "paper"
S = "scissors"

L = "lose"
D = "draw"
W = "win"

shape_scores = {R: 1, P: 2, S: 3}
outcome_scores = {L: 0, D: 3, W: 6}

outcomes = {
    (R, R): D,
    (R, P): L,
    (R, S): W,
    (P, R): W,
    (P, P): D,
    (P, S): L,
    (S, R): L,
    (S, P): W,
    (S, S): D,
}


def part1(text_input):
    their_moves = {"A": R, "B": P, "C": S}
    my_moves = {"X": R, "Y": P, "Z": S}
    total = 0
    for line in text_input.split("\n"):
        their, mine = line.split()
        my_shape = my_moves[mine]
        their_shape = their_moves[their]
        outcome = outcomes[(my_shape, their_shape)]
        total += shape_scores[my_shape] + outcome_scores[outcome]
    return total


def part2(text_input):
    their_moves = {"A": R, "B": P, "C": S}
    outcome_codes = {"X": L, "Y": D, "Z": W}
    # repack the rules to get my shape from their shape and outcome
    my_moves = {
        (their_shape, outcome): my_shape
        for (my_shape, their_shape), outcome in outcomes.items()
    }
    total = 0
    for line in text_input.split("\n"):
        their, outcome = line.split()
        their_shape = their_moves[their]
        outcome = outcome_codes[outcome]
        my_shape = my_moves[(their_shape, outcome)]
        total += shape_scores[my_shape] + outcome_scores[outcome]
    return total
