import argparse
import time


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-d {day}] [--test] [--input {filepath}]",
        description="Solve AdventOfCode2022 puzzles.",
    )
    parser.add_argument(
        "-d",
        "--day",
        type=int,
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
    )
    parser.add_argument("-i", "--input", type=str, help="filepath for input file")
    return parser


def run_day(day, input_path):
    solution = __import__(f"day{day}")
    solution.run(input_path)


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    if args.input is not None:
        if args.day is None:
            print("Please set --day {day} if giving an input file")
        else:
            run_day(args.day, args.input)
    else:
        if args.day is not None:
            days = [args.day]
        else:
            days = list(range(1, 7)) + [21, 22, 23]
        for day in days:
            if args.test:
                args.input = f"inputs/day{day}/test.txt"
            else:
                args.input = f"inputs/day{day}/task.txt"
            t0 = time.perf_counter()
            run_day(day, args.input)
            t1 = time.perf_counter()
            print(f"--- done in {t1-t0:.3f} s")
