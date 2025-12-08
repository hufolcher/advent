import sys
from collections import defaultdict

left_list = []
right_list = []
right_list_appearances = defaultdict(int)

total_weight_carried = [0]
for line in sys.stdin.readlines():
    if line == "\n":
        total_weight_carried.append(0)
    else:
        total_weight_carried[-1] += int(line.strip())

print("", max(total_weight_carried))
print("Part2 is:", sum(sorted(total_weight_carried)[-3:]))
