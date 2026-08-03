from enum import Enum, auto

MIN_STAGE = -6
MAX_STAGE = 6
DEFAULT_STAGE = 0


class Stat(Enum):
    ATTACK = auto()
    DEFENSE = auto()
    SP_ATTACK = auto()
    SP_DEFENSE = auto()
    SPEED = auto()
    ACCURACY = auto()
    EVASION = auto()

    @property
    def stage_base(self) -> int:
        return 3 if self in (Stat.ACCURACY, Stat.EVASION) else 2
