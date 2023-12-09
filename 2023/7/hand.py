from collections import defaultdict

from strenght import Strenght

CARDS = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": -1,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}


def card_max(data: list):
    max = "2"
    for elt in data:
        if CARDS[elt] > CARDS[max]:
            max = elt
    return max


class Hand(str):
    def __new__(cls, value: str, bid: int):
        if len(value) == 5 and all(char in CARDS for char in value):
            instance = super(Hand, cls).__new__(cls, value)
            instance.bid = bid
            return instance
        else:
            raise ValueError("Invalid hand. It should have exactly 5 char from A to 2.")

    def get_strenght(self):
        found_card = defaultdict(int)
        for card in self:
            found_card[card] += 1
        pair_found = False
        three_found = False
        for card, pattern in found_card.items():
            if pattern == 5:
                return Strenght.five_of_a_kind
            elif pattern == 4:
                return Strenght.four_of_a_kind
            elif pattern == 3:
                if pair_found:
                    return Strenght.full_house
                three_found = True
            elif pattern == 2:
                if pair_found:
                    return Strenght.two_pair
                elif three_found:
                    return Strenght.full_house
                pair_found = True
        if pair_found:
            return Strenght.one_pair
        elif three_found:
            return Strenght.three_of_a_kind
        else:
            # print(self)
            return Strenght.hight_card

    def get_part2_strenght(self, debug: bool = False):
        if debug:
            print(self, "->", end=" ")
        finished = False
        while not finished:
            finished, result = self._part2_strenght_step()
            if finished:
                if debug:
                    print(self, result)
                return result
            else:
                self = Hand(result, self.bid)

    def _part2_strenght_step(self):
        found_card = defaultdict(int)
        for card in self:
            found_card[card] += 1

        found_j = found_card["J"]
        del found_card["J"]

        pair_found = False
        pair_value = None
        three_found = False
        three_value = None

        for card, pattern in found_card.items():
            if pattern == 5:
                return True, Strenght.five_of_a_kind

            elif pattern == 4:
                return (
                    (False, self.replace("J", card, found_j))
                    if found_j
                    else (True, Strenght.four_of_a_kind)
                )

            elif pattern == 3:
                if pair_found:
                    return True, Strenght.full_house
                three_value = card
                three_found = True

            elif pattern == 2:
                if pair_found:
                    return (
                        (False, self.replace("J", max(card, pair_value), found_j))
                        if found_j
                        else (True, Strenght.two_pair)
                    )

                elif three_found:
                    return True, Strenght.full_house

                pair_value = card
                pair_found = True

        if pair_found:
            if found_j:
                return False, self.replace("J", pair_value, found_j)
            else:
                return True, Strenght.one_pair

        elif three_found:
            if found_j:
                return False, self.replace("J", three_value, found_j)
            else:
                return True, Strenght.three_of_a_kind
        else:
            if found_j:
                if not len(found_card):
                    return False, self.replace("J", "A", found_j)
                else:
                    return False, self.replace(
                        "J", card_max([key for key in found_card.keys()]), found_j
                    )
            else:
                return True, Strenght.hight_card

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.bid})"

    def __lt__(self, __other) -> bool:
        i = 0
        while i != 5:
            if __other[i] == self[i]:
                i += 1
            elif CARDS[__other[i]] > CARDS[self[i]]:
                return True
            else:
                return False
        return False

    def __gt__(self, __value: str) -> bool:
        return __value.__lt__(self)
