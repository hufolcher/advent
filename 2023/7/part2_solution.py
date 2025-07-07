import os
import sys

folder_path = os.path.dirname(__file__)
utils_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(utils_path))

from hand import Hand
from strenght import Strenght

strenght_map = {
    Strenght.five_of_a_kind: [],
    Strenght.four_of_a_kind: [],
    Strenght.full_house: [],
    Strenght.three_of_a_kind: [],
    Strenght.two_pair: [],
    Strenght.one_pair: [],
    Strenght.hight_card: [],
}

with sys.stdin as file:
    for line in file:
        raw_hand, raw_bid = line.split()
        hand = Hand(raw_hand, int(raw_bid))
        strenght_map[hand.get_part2_strenght(False)] += [hand]

for key in strenght_map.keys():
    strenght_map[key].sort()

final = (
    strenght_map[Strenght.hight_card]
    + strenght_map[Strenght.one_pair]
    + strenght_map[Strenght.two_pair]
    + strenght_map[Strenght.three_of_a_kind]
    + strenght_map[Strenght.full_house]
    + strenght_map[Strenght.four_of_a_kind]
    + strenght_map[Strenght.five_of_a_kind]
)

part2_sum = 0
for index, card in enumerate(final):
    part2_sum += (index + 1) * card.bid

print("Part 2 is:", part2_sum)
