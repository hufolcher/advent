import sys
from collections import defaultdict
from enum import Enum
from typing import List
from functools import cache

class direction(Enum):
    TOP = (-1, 0)
    RIGHT = (0, 1)
    BOTTOM = (1, 0)
    LEFT = (0, -1)

    @property
    def i(self):
        return self.value[0]

    @property
    def j(self):
        return self.value[1]

    def next(self):
        return {
            direction.TOP: direction.RIGHT,
            direction.RIGHT: direction.BOTTOM,
            direction.BOTTOM: direction.LEFT,
            direction.LEFT: direction.TOP,
        }[self]

obstacle = defaultdict(lambda: False)
visited = defaultdict(set)
loop = defaultdict(lambda: False)

data = sys.stdin.read()
lines = data.split("\n")

width = len(lines)
height = len(lines[0])

for i, row in enumerate(lines):
    for j, cell in enumerate(row):
        if cell == "#":
            obstacle[(i, j)] = True
        elif cell == "^":
            starting_i, starting_j = i, j

def walk_step(i,j, direction):
    next_i, next_j = i + direction.i, j + direction.j
    if obstacle[(next_i, next_j)]:
        return i, j, direction.next()
    elif next_i in [-1, width+1] or next_j in [-1, height+1]:
        return False
    else:
        return next_i, next_j, direction

def walk(starting_i, starting_j, starting_direction):
    history = defaultdict(list)
    _next = (starting_i, starting_j, starting_direction)
    while _next:
        if _next[-1] in history[_next[:-1]]:
            return -1
        else:
            history[_next[:-1]].append(_next[-1])
        _next = walk_step(*_next)
    return(history)

std_walk = walk(starting_i, starting_j, direction.TOP)
print("Part 1 is:", len(std_walk))

loops = set()
for new_obstacle_pos in std_walk.keys():
    obstacle[new_obstacle_pos] = True
    if walk(starting_i, starting_j, direction.TOP) == -1:
        loops.add(new_obstacle_pos)
    obstacle[new_obstacle_pos] = False
print("Part 2 is:", len(loops))

#implement the jump !