from collections import defaultdict

left_list = []
right_list = []
right_list_appearances = defaultdict(int)

with open("input.txt", "r") as file:
    for line in file:
        parsed_left, parsed_right = line.strip().split("   ")
        left_list.append(int(parsed_left))
        right_parsed = int(parsed_right)
        right_list.append(right_parsed)
        right_list_appearances[right_parsed] += 1

print("Part1 is:", sum([abs(left - right) for left, right in zip(sorted(left_list),sorted(right_list))]))
print("Part 2 is:", sum([left*right_list_appearances[left] for left in left_list]))