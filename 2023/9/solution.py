import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))


with sys.stdin as file:
    part1_sum = 0
    part2_sum = 0

    for line in file:
        raw = line.strip("\n").split()
        sensor_input = [int(value) for value in raw]
        computed = [sensor_input]
        computation_done = False
        steps = 0
        while not computation_done:
            computed += [[]]
            for i in range(1, len(computed[-2])):
                new = computed[-2][i] - computed[-2][i - 1]
                computed[-1] += [new]
                if new == 0:
                    computation_done = True
                else:
                    computation_done = False
            steps += 1
        computed[-1] += [new]

        part1_extrapolated = [computed[-1]]
        for i in reversed(range(len(computed) - 1)):
            part1_extrapolated += [[computed[i][0]]]
            for difference in part1_extrapolated[-2]:
                part1_extrapolated[-1] += [part1_extrapolated[-1][-1] + difference]

        part1_sum += part1_extrapolated[-1][-1]

        part2_extrapolated = [computed[-1]]
        for i in reversed(range(len(computed) - 1)):
            part2_extrapolated += [[computed[i][-1]]]
            for difference in part2_extrapolated[-2]:
                part2_extrapolated[-1] += [part2_extrapolated[-1][-1] - difference]

        part2_sum += part2_extrapolated[-1][-1]

    print("Part 1 is:", part1_sum)
    print("Part 2 is:", part2_sum)
