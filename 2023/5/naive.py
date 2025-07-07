seed_map = dict()


def convert_from_tuple(seed, tuple):
    _to, _from, lenght = tuple
    if seed >= _from and seed <= _from + lenght:
        return seed + _to - _from


def convert_from_map(seed, list):
    for tuple in list:
        result = convert_from_tuple(seed, tuple)
        if result:
            return result
    return seed


def global_convert(seed, map):
    return convert_from_map(
        convert_from_map(
            convert_from_map(
                convert_from_map(
                    convert_from_map(
                        convert_from_map(
                            convert_from_map(seed, map["seed"]["soil"]),
                            map["soil"]["fertilizer"],
                        ),
                        map["fertilizer"]["water"],
                    ),
                    map["water"]["light"],
                ),
                map["light"]["temperature"],
            ),
            map["temperature"]["humidity"],
        ),
        map["humidity"]["location"],
    )


with sys.stdin as file:
    part1_seeds = [
        int(seed_str) for seed_str in file.readline().split(":")[1].strip().split()
    ]
    file.readline()

    for steps in [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]:
        _from, _to = steps.split("-to-")
        seed_map[_from] = dict()
        seed_map[_from][_to] = list()

        file.readline()
        for line in file:
            if line == "\n":
                break
            else:
                seed_map[_from][_to] += [
                    tuple([int(int_str) for int_str in line.rstrip("\n").split()])
                ]

    print(min([global_convert(seed, seed_map) for seed in part1_seeds]))

    part2_seeds = [
        (part1_seeds[i], part1_seeds[i + 1]) for i in range(0, len(part1_seeds) - 1, 2)
    ]
    min = 15880237
    for pair in part2_seeds:
        _start, _range = pair
        for i in range(_range):
            if i % 100000 == 0:
                print(f"{round(i*100/_range)} %")
            value = global_convert(_start + i, seed_map)
            if value < min:
                min = value
        print(f"{pair} done.")
    print(min)
