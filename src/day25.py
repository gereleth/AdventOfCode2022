# Day 25: Full of Hot Air
# Problem statement: https://adventofcode.com/2022/day/25

day_title = "Full of Hot Air"

char_to_num = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

num_to_char = {num: char for char, num in char_to_num.items()}


def snafu_to_decimal(number_string: str):
    num = 0
    power = 1
    for i in range(1, len(number_string) + 1):
        char = number_string[-i]
        num += char_to_num[char] * power
        power *= 5
    return int(num)


def snafu_place(number):
    power = 0
    max_expressed = 2
    place = 1
    while abs(number) > max_expressed:
        power += 1
        place *= 5
        max_expressed += 2 * place
    quotient = int(round(abs(number) / place)) * (-1 if number < 0 else 1)
    if abs(quotient) <= 2:
        remainder = number - place * quotient
        return power, quotient, remainder
    raise ValueError(f"number {number} power {power} quotient {quotient}")


def decimal_to_snafu(number: int):
    if abs(number) <= 2:
        return num_to_char[number]
    remainder = number
    snafu = ""
    recent_power = 0
    while remainder != 0:
        power, quotient, remainder = snafu_place(remainder)
        if recent_power > power + 1:
            snafu += "0" * (recent_power - power - 1)
        recent_power = power
        snafu += num_to_char[quotient]
    if recent_power > 0:
        snafu += "0" * recent_power
    return snafu


def part1(text_input):
    total = 0
    for line in text_input.split("\n"):
        total += snafu_to_decimal(line)
    return decimal_to_snafu(total)


def part2(text_input):
    return "no task here"


def run(input_path):
    print(f"Day 25: {day_title}")
    with open(input_path) as f:
        content = f.read()
    # test()
    print("Part 1:", part1(content))
    print("Part 2:", part2(content))


def test():
    for number in range(0, 2000):
        snafu = decimal_to_snafu(number)
        decimal = snafu_to_decimal(snafu)
        if number != decimal:
            print(f'ERROR: {number} => "{snafu}" => {decimal}')
            break
