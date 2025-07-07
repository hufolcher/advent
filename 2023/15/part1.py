import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))

if __name__ == "__main__":
    part1_sum = 0
    with sys.stdin as file:
        raw = []
        for line in file:
            raw += line.strip("\n").split(",")

        for command in raw:
            command_hash = 0
            for c in command:
                command_hash += ord(c)
                command_hash *= 17
                command_hash %= 256
            part1_sum += command_hash

        print("Part 1 sum is:", part1_sum)
