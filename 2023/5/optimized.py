import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))
from utils.my_range import MyRange

seed_map = {}
with open(f"{folder_path}/input.txt", "r") as file:
    raw_seed_int_list = [
        int(seed_str) for seed_str in file.readline().split(":")[1].strip().split()
    ]
    part1_seeds = [MyRange(seed) for seed in raw_seed_int_list]

    part2_seeds = [
        MyRange(seed_pair[0], sum(seed_pair) - 1)
        for seed_pair in [
            tuple(raw_seed_int_list[i : i + 2])
            for i in range(0, len(raw_seed_int_list), 2)
        ]
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
                _s1, _s2, _s3 = line.rstrip("\n").split()
                _to_start, _from_start, lenght = int(_s1), int(_s2), int(_s3)
                seed_map[_from][_to] += [
                    (
                        MyRange(_from_start, _from_start + lenght - 1),
                        _to_start - _from_start,
                    )
                ]

SEED_MAP = seed_map


def convert_from_tuple(to_process: list[MyRange], tuple: tuple[range]):
    _from, _offset = tuple
    processed, unprocessed = [], []
    for interval in to_process:
        inside, outside = interval.mask(_from)
        processed += [elt.offset(_offset) for elt in inside]
        unprocessed += outside
    return processed, unprocessed


def convert_from_map(to_process: list, step: list):
    result = []
    unprocessed = to_process
    for tuple in step:
        processed, unprocessed = convert_from_tuple(unprocessed, tuple)
        if processed:
            result += processed
    result += unprocessed
    return result


def global_convert(seed_range: MyRange):
    return convert_from_map(
        convert_from_map(
            convert_from_map(
                convert_from_map(
                    convert_from_map(
                        convert_from_map(
                            convert_from_map(seed_range, SEED_MAP["seed"]["soil"]),
                            SEED_MAP["soil"]["fertilizer"],
                        ),
                        SEED_MAP["fertilizer"]["water"],
                    ),
                    SEED_MAP["water"]["light"],
                ),
                SEED_MAP["light"]["temperature"],
            ),
            SEED_MAP["temperature"]["humidity"],
        ),
        SEED_MAP["humidity"]["location"],
    )


print("Part 1 result is:", min(global_convert(part1_seeds)).start)
print("Part 2 result is:", min(global_convert(part2_seeds)).start)
