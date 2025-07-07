import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))


def score(column):
    score = 0
    current_line_score = len(column)
    for index, elt in enumerate(column):
        if elt == "O":
            score += current_line_score
            current_line_score -= 1
        elif elt == ".":
            pass
        elif elt == "#":
            current_line_score = len(column) - (index + 1)
    return score


if __name__ == "__main__":
    with sys.stdin as file:
        raw = []
        for line in file:
            raw += [line.strip("\n")]

        part1_sum = 0
        for column in zip(*raw):
            part1_sum += score(column)
        print("Part 1 is:", part1_sum)
