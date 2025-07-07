import sys

part2_pokedex = [0] * 500  # up to 500 Cards


def raw_to_int_list(raw: str):
    return [int(string) for string in raw.strip().split()]


with sys.stdin as file:
    part1_sum = 0
    for line in file:
        raw_line_id, data = line.split(":")
        line_id = int(raw_line_id.split(" ")[-1])
        raw_wins, raw_draws = data.split("|")
        wins = raw_to_int_list(raw_wins)
        draws = raw_to_int_list(raw_draws)

        part2_match = 0
        part1_score = 0
        part2_pokedex[line_id] += 1

        for draw in draws:
            if draw in wins:
                part2_match += 1
                if part1_score == 0:
                    part1_score = 1
                else:
                    part1_score *= 2

        for i in range(1, part2_match + 1):
            part2_pokedex[line_id + i] += part2_pokedex[line_id]
        part1_sum += part1_score


print(part1_sum)
print(sum(part2_pokedex))
