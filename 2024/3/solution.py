import sys

import re

s1 = 0
s2 = 0
with sys.stdin as file:
    part2_enabled = True
    for expression in re.split(r"(don\'t\(\)|do\(\))", "".join(file)):
        if expression == "don't()":
            part2_enabled = False
        elif expression == "do()":
            part2_enabled = True
        else:
            increment = sum(
                [
                    int(group.group(1)) * int(group.group(2))
                    for group in re.finditer(r"mul\((\d+),(\d+)\)", expression)
                ]
            )
            s1 += increment
            if part2_enabled:
                s2 += increment

print("", s1)
print("Part 2 is:", s2)
