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


def decimal_to_snafu(number: int):
    # single-digit case
    if abs(number) <= 2:
        return num_to_char[number]
    # do I even need to care about negative numbers?..
    if number < 0:
        snafu = decimal_to_snafu(abs(number))
        res = "".join(num_to_char[-char_to_num[char]] for char in snafu)
        return res
    # build the snafu number from right to left
    remaining = number
    snafu = ""
    carry = 0
    while remaining != 0:
        remaining, last_digit = divmod(remaining, 5)
        last_digit += carry
        carry = 0
        if last_digit >= 3:
            carry = 1
            last_digit = last_digit - 5
        snafu = num_to_char[last_digit] + snafu
    if carry == 1:
        snafu = "1" + snafu
    return snafu


def part1(text_input):
    total = 0
    for line in text_input.split("\n"):
        total += snafu_to_decimal(line)
    return decimal_to_snafu(total)


def part2(text_input):
    return "no task here"


def test():
    for sign in [1, -1]:
        for number in range(2000):
            n = number * sign
            snafu = decimal_to_snafu(n)
            decimal = snafu_to_decimal(snafu)
            if n != decimal:
                print(f'ERROR: {n} => "{snafu}" => {decimal}')
                break


if __name__ == "__main__":
    test()
