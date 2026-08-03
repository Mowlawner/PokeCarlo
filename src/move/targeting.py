from enum import Enum, auto


class MoveTarget(Enum):
    SINGLE_TARGET = auto()
    SELF = auto()
    ALL_OTHERS = auto()
    ALL = auto()
    ALL_OPPONENTS = auto()
    RANDOM_OPPONENT = auto()
    ALL_ALLIES = auto()
    FIELD = auto()
