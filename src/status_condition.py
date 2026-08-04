# status_condition.py

from enum import Enum, auto


class StatusCondition(Enum):
    NONE = auto()
    BURN = auto()
    PARALYSIS = auto()
    SLEEP = auto()
    FREEZE = auto()
    POISON = auto()
    BAD_POISON = auto()
