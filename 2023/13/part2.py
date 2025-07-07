import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))


def part2_same(left_pattern: list, right_pattern: list):
    left = left_pattern
    right = right_pattern
    smudge_fixed = False
    for left_elt, right_elt in zip(left, right):
        if left_elt != right_elt:
            if (
                not smudge_fixed
                and sum(1 for a, b in zip(left_elt, right_elt) if a != b) == 1
            ):
                smudge_fixed = True
            else:
                return False
    return smudge_fixed


def symetry_from_pattern(pattern):
    for i in range(1, len(pattern)):
        if part2_same(list(reversed(pattern[:i])), pattern[i:]):
            return True, i
    return False, None


if __name__ == "__main__":
    with sys.stdin as file:
        part1_sum = 0
        raw_patterns = [[]]
        for line in file:
            if line == "\n":
                raw_patterns += [[]]
            else:
                raw_patterns[-1] += [line.strip("\n")]

        for raw_pattern in raw_patterns:
            LINE_LENGHT = len(raw_pattern[0])

            horizontals = ["".join(line) for line in raw_pattern]
            verticals = [
                "".join(line[i] for line in raw_pattern) for i in range(LINE_LENGHT)
            ]

            horizontal_found, index = symetry_from_pattern(horizontals)
            if horizontal_found:
                print(
                    "horizontal symetry at indexes:",
                    f"{index}-{index+1}",
                    ", score +=",
                    (index) * 100,
                )
                part1_sum += (index) * 100
            else:
                vertical_found, index = symetry_from_pattern(verticals)
                assert vertical_found
                print(
                    "vertical symetry at indexes:",
                    f"{index}-{index+1}",
                    ", score +=",
                    index,
                )
                part1_sum += index

        print("Part 1 score is:", part1_sum)
