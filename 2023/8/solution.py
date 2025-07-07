import math
import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))

NODE_MAP = dict()
INSTRUCTIONS = ""


def lcm_of_list(numbers):
    def lcm(x, y):
        return x * y // math.gcd(x, y)

    result = 1
    for number in numbers:
        result = lcm(result, number)
    return result


def solve(current, count, debug):
    for instruction in INSTRUCTIONS:
        if debug:
            print(f"for {instruction}: {current} ({count})", "-> ", end="")
        current = NODE_MAP[current][0 if instruction == "L" else 1]
        count += 1
        if debug:
            print(f"{current} ({count})")
    return current, count


with sys.stdin as file:
    INSTRUCTIONS = file.readline().strip()
    file.readline()
    starts = []

    for line in file:
        raw = line.strip("\n").split("=")
        raw_left, raw_right = raw[1].strip().split(",")
        current = raw[0].strip()
        NODE_MAP[raw[0].strip()] = (raw_left[1:], raw_right[:-1].strip())
        if current[2] == "A":
            starts += [current]


result = []
for start in starts:
    current = start
    count = 0
    while current[2] != "Z":
        current, count = solve(current, count, False)
    result += [count]

print("Part 1 is:", min(result))
print("Part 2 is:", lcm_of_list(result))
