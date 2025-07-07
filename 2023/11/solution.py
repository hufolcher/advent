import os
import sys
from collections import defaultdict
from itertools import combinations

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))

PRIMORDIAL_TO_REAL_UNIVERSE_MAP = defaultdict(tuple)
GALAXIES = []
EXPAND_FACTOR = 1000000 - 1


def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def debug_print_universe():
    for i in range(line_nb):
        print(
            [
                "#" if PRIMORDIAL_TO_REAL_UNIVERSE_MAP[(i, j)] else "."
                for j in range(line_size)
            ]
        )


with sys.stdin as file:
    raw = []
    for i, line in enumerate(file):
        universe_line = line.strip("\n")
        raw += [universe_line]
    line_nb = len(raw)
    line_size = len(raw[0])

    expand_i = 0
    expand_j = 0
    galaxy_found_in_column = False

    for i, line in enumerate(raw):
        galaxy_found = False
        for j in range(line_size):
            if line[j] == "#":
                PRIMORDIAL_TO_REAL_UNIVERSE_MAP[(i, j)] = (expand_i, 0)
                galaxy_found = True
                GALAXIES += [(i, j)]
        if not galaxy_found:
            expand_i += EXPAND_FACTOR

    for j in range(line_size):
        galaxy_found = False
        for i, line in enumerate(raw):
            if line[j] == "#":
                expand_i, _ = PRIMORDIAL_TO_REAL_UNIVERSE_MAP[(i, j)]
                PRIMORDIAL_TO_REAL_UNIVERSE_MAP[(i, j)] = (expand_i, expand_j)
                galaxy_found = True
        if not galaxy_found:
            expand_j += EXPAND_FACTOR

    MAX_J = len(PRIMORDIAL_TO_REAL_UNIVERSE_MAP)
    MAX_I = i + 1

    print(
        f"For expand factor '{EXPAND_FACTOR}' result is:",
        sum(
            [
                manhattan_distance(
                    tuple(
                        x + y
                        for x, y in zip(_from, PRIMORDIAL_TO_REAL_UNIVERSE_MAP[_from])
                    ),
                    tuple(
                        x + y for x, y in zip(_to, PRIMORDIAL_TO_REAL_UNIVERSE_MAP[_to])
                    ),
                )
                for _from, _to in list(combinations(GALAXIES, 2))
            ]
        ),
    )
