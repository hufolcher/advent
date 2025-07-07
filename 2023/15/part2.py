import os
import sys
from collections import defaultdict, OrderedDict

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))


def hash(label: str):
    hash = 0
    for c in label:
        hash += ord(c)
        hash *= 17
        hash %= 256
    return hash


MAP = defaultdict(OrderedDict)

if __name__ == "__main__":
    part2_sum = 0
    with sys.stdin as file:
        raw = []
        for line in file:
            raw += line.strip("\n").split(",")

        for command in raw:

            if "=" in command:
                label, str_value = command.split("=")
                MAP[hash(label)][label] = int(str_value)
            if "-" in command:
                label = command.strip("-")
                box = MAP[hash(label)]
                if label in box:
                    del box[label]
            command_hash = 0

        for _hash, _box in MAP.items():
            for index, label in enumerate(_box):
                part2_sum += _box[label] * (index + 1) * (_hash + 1)

        print("Part 2 sum is:", part2_sum)
