import sys

tab = []

with sys.stdin as file:
    for line in file:
        tab += [[char for char in line.rstrip("\n")]]

TAB = tab
INLINE_SIZE = len(TAB[0])
TAB_SIZE = len(TAB)

GEARS = {}


def is_adjacent(line_index, inline_index):
    for i in range(line_index - 1, line_index + 2):
        for j in range(inline_index - 1, inline_index + 2):
            if i >= 0 and i < TAB_SIZE:
                if j >= 0 and j < INLINE_SIZE:
                    if TAB[i][j] != "." and not TAB[i][j].isdigit():
                        return True
    return False


def compute_for_gear(value, line_index_range, inline_index_range):
    for i in line_index_range:
        for j in inline_index_range:
            if i >= 0 and i < TAB_SIZE:
                if j >= 0 and j < INLINE_SIZE:
                    if TAB[i][j] == "*":
                        if (i, j) not in GEARS:
                            GEARS[(i, j)] = [value]
                        else:
                            GEARS[(i, j)] += [value]


part1_sum = 0

for line_index in range(TAB_SIZE):
    current = ""
    valid = False
    for inline_index in range(INLINE_SIZE):
        char = TAB[line_index][inline_index]
        if char.isdigit():
            current += char
            if not valid:
                valid = is_adjacent(line_index, inline_index)

        if not char.isdigit() or inline_index == INLINE_SIZE - 1:
            if len(current) != 0:
                if valid:
                    value = int(current)
                    part1_sum += value
                    compute_for_gear(
                        value,
                        [line_index - 1, line_index, line_index + 1],
                        [
                            index
                            for index in range(
                                inline_index - len(current) - 1, inline_index + 1
                            )
                        ],
                    )
                current = ""
                valid = False
print("Part 1:", part1_sum)

part2_sum = 0
for associates in GEARS.values():
    if len(associates) == 2:
        gears_power = 1
        for value in associates:
            gears_power *= value
        part2_sum += gears_power
print("Part 2:", part2_sum)
