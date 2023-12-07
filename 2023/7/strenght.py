from enum import IntEnum, auto

class Strenght(IntEnum):
    five_of_a_kind = 0
    four_of_a_kind = auto()
    full_house = auto()
    three_of_a_kind = auto()
    two_pair = auto()
    one_pair = auto()
    hight_card = auto()

    def __str__(self) -> str:
        return self.name

