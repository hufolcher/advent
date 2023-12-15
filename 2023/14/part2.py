import os
import sys

from functools import cache

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))

def part2_score(column):
    score = 0
    for index, elt in enumerate(column):
        if elt == "O":
            score += len(column) - (index)
    return(score)

@cache
def roll_east(line: str):
    rock_in_bag = 0
    void_in_bag = 0
    new_line = ""
    for index in range(len(line)):
        if line[index] == "O":
            rock_in_bag += 1
        elif line[index] == ".":
            void_in_bag += 1
        elif line[index] == "#":
            new_line += "." * void_in_bag + "O" * rock_in_bag + "#"
            rock_in_bag, void_in_bag = 0, 0
    new_line += "." * void_in_bag + "O" * rock_in_bag
    return(new_line)

@cache
def cycle(raw):
    north = []
    for column in zip(*raw):
        north += [roll_east("".join(column[::-1]))[::-1]]
    west = []
    for column in zip(*north):
        west += [roll_east("".join(column[::-1]))[::-1]]
    south = []
    for column in zip(*west):
        south += [roll_east("".join(column))]
    east = []
    for column in zip(*south):
        east += [roll_east("".join(column))]
    return(tuple(east))


if __name__ == "__main__":
    with open(f"{folder_path}/input.txt", "r") as file:
        raw = []
        for line in file:
            raw += [line.strip("\n")]



        tab = tuple(raw)
        tabs = []
        for i in range((1000000000-110)%18 + 92):
            tab = cycle(tab)

        part2_sum = 0
        for column in (zip(*tab)):
            part2_sum += part2_score(column)

        print("Part 2 is:", part2_sum)

        # for i in range((1000000000-110)%18 + 92):
        #     tab = cycle(tab)
        #     part2_sum = 0
        #     found = False
        #     for j in range(len(tabs)):
        #         if tabs[j] == tab:
        #             print("match for:", i, j)
        #             break
        #     if not found:
        #         tabs += [tab]
        #     else:
        #         break
