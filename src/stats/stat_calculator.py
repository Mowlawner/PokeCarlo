from stats.base_stats import BaseStats
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature
from stats.stat import Stat
from stats.stats import Stats


def calculate_hp(
    base: int,
    iv: int,
    ev: int,
    level: int,
) -> int:
    """
    Calculates HP for a Pokemon.

    Formula:
    floor(((2 * Base + IV + EV//4) * Level) / 100) + Level + 10
    """

    return ((2 * base + iv + ev // 4) * level) // 100 + level + 10


def calculate_non_hp_stat(
    base: int,
    iv: int,
    ev: int,
    level: int,
    nature_modifier: float,
) -> int:
    """
    Calculates a non-HP stat.

    Formula:
    floor(
        (floor(((2 * Base + IV + EV//4) * Level) / 100) + 5)
        * Nature
    )
    """

    raw_stat = ((2 * base + iv + ev // 4) * level) // 100 + 5

    return int(raw_stat * nature_modifier)


def get_nature_modifier(
    nature: Nature,
    stat: Stat,
) -> float:
    if nature.increased_stat == stat:
        return 1.1

    if nature.decreased_stat == stat:
        return 0.9

    return 1.0


def calculate_stats(
    base_stats: BaseStats,
    ivs: IVs,
    evs: EVs,
    nature: Nature,
    level: int,
) -> Stats:

    return Stats(
        hp=calculate_hp(
            base_stats.hp,
            ivs.hp,
            evs.hp,
            level,
        ),
        attack=calculate_non_hp_stat(
            base_stats.attack,
            ivs.attack,
            evs.attack,
            level,
            get_nature_modifier(nature, Stat.ATTACK),
        ),
        defense=calculate_non_hp_stat(
            base_stats.defense,
            ivs.defense,
            evs.defense,
            level,
            get_nature_modifier(nature, Stat.DEFENSE),
        ),
        sp_attack=calculate_non_hp_stat(
            base_stats.sp_attack,
            ivs.sp_attack,
            evs.sp_attack,
            level,
            get_nature_modifier(nature, Stat.SP_ATTACK),
        ),
        sp_defense=calculate_non_hp_stat(
            base_stats.sp_defense,
            ivs.sp_defense,
            evs.sp_defense,
            level,
            get_nature_modifier(nature, Stat.SP_DEFENSE),
        ),
        speed=calculate_non_hp_stat(
            base_stats.speed,
            ivs.speed,
            evs.speed,
            level,
            get_nature_modifier(nature, Stat.SPEED),
        ),
    )
