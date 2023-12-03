MAX = {"red": 12, "green": 13, "blue": 14}

def test_from_set(set: list):
    for run in set:
        if int(run[0]) > MAX[run[1]]:
            return False
    return True

def power_from_sets(sets: list):
    max_red = 1
    max_green = 1
    max_blue = 1
    flattened = [item for sublist in sets for item in sublist]

    for run in flattened:
        if run[1] == "red":
            max_red = max(max_red, int(run[0]))
        elif run[1] == "green":
            max_green = max(max_green, int(run[0]))
        elif run[1] == "blue":
            max_blue = max(max_blue, int(run[0]))
    return(max_red*max_blue*max_green)

with open("input.txt", "r") as file:
    possible_id_sum = 0
    power_sum = 0

    for line in file:
        id_from_data = line.rstrip("\n").split(":")
        games = id_from_data[1].split(";")
        sets = [list(map(lambda string: string.strip().split(" "), game.split(","))) for game in games]
        if all([test_from_set(set) for set in sets]):
            possible_id_sum += int(id_from_data[0].split(" ")[1])
        power_sum += power_from_sets(sets)

    print(possible_id_sum)
    print(power_sum)