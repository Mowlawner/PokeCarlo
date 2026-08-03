from enum import Enum, auto

from stats.stat import Stat


class Nature(Enum):
    HARDY = auto()
    LONELY = auto()
    BRAVE = auto()
    ADAMANT = auto()
    NAUGHTY = auto()

    BOLD = auto()
    DOCILE = auto()
    RELAXED = auto()
    IMPISH = auto()
    LAX = auto()

    TIMID = auto()
    HASTY = auto()
    SERIOUS = auto()
    JOLLY = auto()
    NAIVE = auto()

    MODEST = auto()
    MILD = auto()
    QUIET = auto()
    BASHFUL = auto()
    RASH = auto()

    CALM = auto()
    GENTLE = auto()
    SASSY = auto()
    CAREFUL = auto()
    QUIRKY = auto()

    @property
    def increased_stat(self) -> Stat | None:
        return _INCREASED_STAT_BY_NATURE.get(self)

    @property
    def decreased_stat(self) -> Stat | None:
        return _DECREASED_STAT_BY_NATURE.get(self)


_INCREASED_STAT_BY_NATURE: dict[Nature, Stat] = {
    Nature.LONELY: Stat.ATTACK,
    Nature.BRAVE: Stat.ATTACK,
    Nature.ADAMANT: Stat.ATTACK,
    Nature.NAUGHTY: Stat.ATTACK,
    Nature.BOLD: Stat.DEFENSE,
    Nature.RELAXED: Stat.DEFENSE,
    Nature.IMPISH: Stat.DEFENSE,
    Nature.LAX: Stat.DEFENSE,
    Nature.TIMID: Stat.SPEED,
    Nature.HASTY: Stat.SPEED,
    Nature.JOLLY: Stat.SPEED,
    Nature.NAIVE: Stat.SPEED,
    Nature.MODEST: Stat.SP_ATTACK,
    Nature.MILD: Stat.SP_ATTACK,
    Nature.QUIET: Stat.SP_ATTACK,
    Nature.RASH: Stat.SP_ATTACK,
    Nature.CALM: Stat.SP_DEFENSE,
    Nature.GENTLE: Stat.SP_DEFENSE,
    Nature.SASSY: Stat.SP_DEFENSE,
    Nature.CAREFUL: Stat.SP_DEFENSE,
}

_DECREASED_STAT_BY_NATURE: dict[Nature, Stat] = {
    Nature.LONELY: Stat.DEFENSE,
    Nature.BRAVE: Stat.SPEED,
    Nature.ADAMANT: Stat.SP_ATTACK,
    Nature.NAUGHTY: Stat.SP_DEFENSE,
    Nature.BOLD: Stat.ATTACK,
    Nature.RELAXED: Stat.SPEED,
    Nature.IMPISH: Stat.SP_ATTACK,
    Nature.LAX: Stat.SP_DEFENSE,
    Nature.TIMID: Stat.ATTACK,
    Nature.HASTY: Stat.DEFENSE,
    Nature.JOLLY: Stat.SP_ATTACK,
    Nature.NAIVE: Stat.SP_DEFENSE,
    Nature.MODEST: Stat.ATTACK,
    Nature.MILD: Stat.DEFENSE,
    Nature.QUIET: Stat.SPEED,
    Nature.RASH: Stat.SP_DEFENSE,
    Nature.CALM: Stat.ATTACK,
    Nature.GENTLE: Stat.DEFENSE,
    Nature.SASSY: Stat.SPEED,
    Nature.CAREFUL: Stat.SP_ATTACK,
}
