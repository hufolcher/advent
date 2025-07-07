import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))


def layout(line: str):
    result = []
    last = None
    for c in line:
        if c == "#":
            if last == "#":
                result[-1] += 1
            else:
                result += [1]
        last = c
    return tuple(result)


def replace(line: str, binary_repr, _to="#", _from="?"):
    test_line = list(line)
    c = 0
    for i in range(len(test_line)):
        if c != len(binary_repr):
            if test_line[i] == _from:
                test_line[i] = _to if binary_repr[c] == "1" else "."
                c += 1
        else:
            break
    return "".join(test_line)


def solve_line(line, target_layout):
    mystery_count = 0
    for elt in line:
        if elt == "?":
            mystery_count += 1

    ways = 0
    for i in range(2**mystery_count):
        if (
            layout(replace(line, "{:0>{}}".format(bin(i)[2:], mystery_count)))
            == target_layout
        ):
            ways += 1
    return ways


if __name__ == "__main__":
    with sys.stdin as file:
        part1_sum = 0
        for i, line in enumerate(file):
            raw_line, raw_target_layout = line.strip("\n").split()

            line = list(raw_line)
            target_layout = [int(raw_str) for raw_str in raw_target_layout.split(",")]

            part1_sum += solve_line("".join(line), tuple(target_layout))

        print("Part 1 is:", part1_sum)
