import os
import sys
from collections import defaultdict

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))

from enum import StrEnum

box = {
    "-": chr(0x2500),
    "|": chr(0x2502),
    "L": chr(0x2514),
    "F": chr(0x250C),
    "7": chr(0x2510),
    "J": chr(0x2518),
    ".": ".",
    "S": "S",
}


class Pattern(StrEnum):
    START = "S"
    GROUND = "."
    HORIZONTAL = "-"
    VERTICAL = "|"
    UP_LEFT = "J"
    UP_RIGHT = "L"
    DOWN_RIGHT = "F"
    DOWN_LEFT = "7"

    def __str__(self) -> str:
        return box[self.value]

    def __repr__(self) -> str:
        return box[self.value]


def debug_print(data):
    for line in data:
        print("".join([box[elt] for elt in line]))


WORLD = []

with open(f"{folder_path}/input.txt", "r") as file:
    for i, line in enumerate(file):
        world_line = [Pattern(string) for string in line.strip("\n")]
        WORLD += [[Pattern.GROUND] + world_line + [Pattern.GROUND]]
        if Pattern.START in world_line:
            start_i, start_j = i + 1, world_line.index(Pattern.START) + 1

    WORLD = (
        [[Pattern.GROUND] * len(WORLD[0])] + WORLD + [[Pattern.GROUND] * len(WORLD[0])]
    )
    world_max_i, world_max_j = len(WORLD), len(WORLD[0])

    def get_paths(node_i, node_j, pattern: Pattern):
        result = []
        if pattern in [
            Pattern.UP_LEFT,
            Pattern.UP_RIGHT,
            Pattern.START,
            Pattern.VERTICAL,
        ]:
            i, j = node_i - 1, node_j
            if WORLD[i][j] in [
                Pattern.DOWN_LEFT,
                Pattern.DOWN_RIGHT,
                Pattern.VERTICAL,
                Pattern.START,
            ]:
                result += [(i, j, WORLD[i][j])]
        if pattern in [
            Pattern.DOWN_LEFT,
            Pattern.DOWN_RIGHT,
            Pattern.START,
            Pattern.VERTICAL,
        ]:
            i, j = node_i + 1, node_j
            if WORLD[i][j] in [
                Pattern.UP_LEFT,
                Pattern.UP_RIGHT,
                Pattern.VERTICAL,
                Pattern.START,
            ]:
                result += [(i, j, WORLD[i][j])]
        if pattern in [
            Pattern.DOWN_LEFT,
            Pattern.UP_LEFT,
            Pattern.START,
            Pattern.HORIZONTAL,
        ]:
            i, j = node_i, node_j - 1
            if WORLD[i][j] in [
                Pattern.UP_RIGHT,
                Pattern.DOWN_RIGHT,
                Pattern.HORIZONTAL,
                Pattern.START,
            ]:
                result += [(i, j, WORLD[i][j])]
        if pattern in [
            Pattern.DOWN_RIGHT,
            Pattern.UP_RIGHT,
            Pattern.START,
            Pattern.HORIZONTAL,
        ]:
            i, j = node_i, node_j + 1
            if WORLD[i][j] in [
                Pattern.UP_LEFT,
                Pattern.DOWN_LEFT,
                Pattern.HORIZONTAL,
                Pattern.START,
            ]:
                result += [(i, j, WORLD[i][j])]
        return result

    starts = get_paths(start_i, start_j, Pattern.START)
    i_from, j_from = start_i, start_j
    i, j, pattern = starts[0]
    LOOP = []
    LOOP_MAP = defaultdict(bool)
    LOOP_MAP[(start_i, start_j)] = True

    while pattern != Pattern.START:
        for _i, _j, _pattern in get_paths(i, j, pattern):
            if _i != i_from or _j != j_from:
                LOOP += [(i, j, pattern)]
                LOOP_MAP[(i, j)] = True
                i_from, j_from = i, j
                i, j, pattern = _i, _j, _pattern
                break

    debug_print(WORLD)

    print("Part 1 farthest:", len(LOOP) // 2 + 1)

    inside = 0
    for i in range(world_max_i):
        for j in range(world_max_j):
            is_in = False
            for tested_j in range(j + 1, world_max_j):
                if not LOOP_MAP[(i, j)]:
                    if LOOP_MAP[(i, tested_j)] and WORLD[i][tested_j] in [
                        Pattern.VERTICAL,
                        Pattern.UP_LEFT,
                        Pattern.UP_RIGHT,
                    ]:
                        is_in = not is_in
            if is_in:
                inside += 1

    print("Part 2 inside:", inside)
