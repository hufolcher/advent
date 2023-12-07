import math
import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))

EPSILON = 0.00000001

with open(f"{folder_path}/input.txt", "r") as file:
    part1_time_int_list = [
        int(time_str) for time_str in file.readline().split(":")[1].strip().split()
    ]
    part1_distance_int_list = [
        int(distance_str)
        for distance_str in file.readline().split(":")[1].strip().split()
    ]
    part2_time_str = ""
    for elt in part1_time_int_list:
        part2_time_str += str(elt)

    part2_distance_str = ""
    for elt in part1_distance_int_list:
        part2_distance_str += str(elt)

    part2_time_int_list = [int(part2_time_str)]
    part2_distance_int_list = [int(part2_distance_str)]

    def solve(time_list, distance_list):
        total_prod = 1

        for time, distance in zip(time_list, distance_list):
            delta = time**2 - 4 * distance
            sr_delta = delta**0.5

            if delta > 0:
                solution1, solution2 = (-1 * time + sr_delta) / (-2), (
                    -1 * time - sr_delta
                ) / (-2)
                threshold1, threshold2 = max(0, math.ceil(solution1 + EPSILON)), max(
                    0, math.floor(solution2 - EPSILON)
                )
                ways = threshold2 - threshold1 + 1
            else:
                ways *= 0
            total_prod *= ways

        return total_prod

    print("Part 1 result is:", solve(part1_time_int_list, part1_distance_int_list))
    print("Part 2 result is:", solve(part2_time_int_list, part2_distance_int_list))
