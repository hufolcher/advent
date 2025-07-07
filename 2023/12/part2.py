import os
import sys
from functools import cache

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))

OPERATIONNAL = "."
BROKEN = "#"
UNKNOWN = "?"

DOUBT = [BROKEN, UNKNOWN]

EXPAND_FACTOR = 5


@cache
def count(springs: str, layout: tuple):
    if len(layout) == 0:
        return BROKEN not in springs

    if len(springs) == 0:
        return 0

    first = springs[0]
    if first == OPERATIONNAL:
        return count(springs[1:], layout)

    if first == UNKNOWN:
        return count(springs[1:], layout) + count(BROKEN + springs[1:], layout)

    if first == BROKEN:
        i = 0
        while i < len(springs) and i < layout[0] and springs[i] in DOUBT:
            i += 1

        if i == len(springs):
            return len(layout) == 1 and i == layout[0]

        elif i != layout[0]:
            return 0

        elif springs[i] == BROKEN:
            return 0

        else:
            return count(springs[i + 1 :], layout[1:])


with sys.stdin as file:
    part1_sum = 0
    part2_sum = 0

    for line_index, line in enumerate(file):
        print(line_index)
        raw_line, raw_target_layout = line.strip("\n").split()

        springs = raw_line + (UNKNOWN + raw_line) * (EXPAND_FACTOR - 1)
        target_layout = tuple(
            [int(raw_str) for raw_str in raw_target_layout.split(",")] * EXPAND_FACTOR
        )

        part2_sum += count(springs, target_layout)

    print("Part 2 is:", part2_sum)
