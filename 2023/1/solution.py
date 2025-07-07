import sys

_map = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}


def compute(data: str):
    digit_list = [char for char in data if char.isdigit()]
    return int(f"{digit_list[0]}{digit_list[-1]}")


with sys.stdin as file:
    sum_1 = 0
    sum_2 = 0
    for line in file:
        sum_1 += compute(line)

        for key, value in _map.items():
            line = line.replace(value, f"{value}{key}{value}")
        sum_2 += compute(line)

print(sum_1)
print(sum_2)
