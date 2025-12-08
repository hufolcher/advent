import sys

round_to_score_part1 = {
    "A": {"X": 3 + 1, "Y": 6 + 2, "Z": 0 + 3},
    "B": {"X": 0 + 1, "Y": 3 + 2, "Z": 6 + 3},
    "C": {"X": 6 + 1, "Y": 0 + 2, "Z": 3 + 3},
}
round_to_score_part2 = {
    "A": {"X": 0 + 3, "Y": 3 + 1, "Z": 6 + 2},
    "B": {"X": 0 + 1, "Y": 3 + 2, "Z": 6 + 3},
    "C": {"X": 0 + 2, "Y": 3 + 3, "Z": 6 + 1},
}

score_part1 = 0
score_part2 = 0
for line in sys.stdin.readlines():
    first, second = line.strip().split(" ")
    score_part1 += round_to_score_part1[first][second]
    score_part2 += round_to_score_part2[first][second]

print("", score_part1)
print("Part2 is:", score_part2)
