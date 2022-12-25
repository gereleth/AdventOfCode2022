# Advent of Code 2022

My python solutions for [Advent Of Code 2022](https://adventofcode.com/2022).

Days already added to the repo:

| Mo     | Tu     | We     | Th     | Fr     | Sa     | Su     |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
|        |        |        | ~~1~~  | ~~2~~  | ~~3~~  | ~~4~~  |
| ~~5~~  | ~~6~~  | ~~7~~  | **8**  | **9**  | **10** | **11** |
| **12** | **13** | **14** | **15** | **16** | **17** | **18** |
| ~~19~~ | ~~20~~ | ~~21~~ | ~~22~~ | ~~23~~ | ~~24~~ | ~~25~~ |

## Prerequisites

I ran this code on python 3.10.8. It might work on other python 3 versions too.

Create a virtual environment and install dependencies.

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Layout

Code for each day is in `src/day{i}.py`.

Inputs for each day are in `inputs/day{i}/test.txt` and `inputs/day{i}/task.txt`.

## Usage

Solve all tasks:

```bash
python src/solve.py
```

Solve particular day:

```bash
python src/solve.py --day {day}
```

Other options:

- `--test` - run on test input
- `--day {day} --input {filepath}` - run on a specified input file
