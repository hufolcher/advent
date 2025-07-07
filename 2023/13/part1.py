import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))


def pattern_from_raw(raw):
    pattern = []
    last = None
    for elt in raw:
        if last == elt:
            pattern[-1] = (elt, pattern[-1][1] + 1)
        else:
            pattern += [(elt, 1)]
        last = elt
    return pattern


def flatten(pattern):
    result = []
    for sub_list in [[elt[0]] * elt[1] for elt in pattern]:
        result += sub_list
    return result


def part1_same(left_pattern: list, right_pattern: list):
    left = flatten(left_pattern)
    right = flatten(right_pattern)
    return all([left_elt == right_elt for left_elt, right_elt in zip(left, right)])


def symetry_from_pattern(pattern):
    true_index = 0
    for i in range(len(pattern)):
        if pattern[i][1] % 2 == 0:
            if part1_same(list(reversed(pattern[:i])), pattern[i + 1 :]):
                return True, true_index + pattern[i][1] // 2
        true_index += pattern[i][1]
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

            horizontals = pattern_from_raw(["".join(line) for line in raw_pattern])
            verticals = pattern_from_raw(
                ["".join(line[i] for line in raw_pattern) for i in range(LINE_LENGHT)]
            )

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
