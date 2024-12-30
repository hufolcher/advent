from collections import defaultdict

left_list = []
right_list = []
right_list_appearances = defaultdict(int)

total_weight_carried = [0]
with open("input.txt", "r") as file:
    for line in file:
        if line == "\n":
            total_weight_carried.append(0)
        else:
            total_weight_carried[-1] += int(line.strip())

print("Part1 is:", max(total_weight_carried))
print("Part2 is:", sum(sorted(total_weight_carried)[-3:]))