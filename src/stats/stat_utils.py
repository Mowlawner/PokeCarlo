from base_stats.stat import MAX_STAGE, MIN_STAGE, Stat
from base_stats.stat_stages import StatStages


def get_stage(stages: StatStages, stat: Stat) -> int:
    """
    Finds the stat stage specified in `stat`.

    :param stages: The StatStages object to read from.
    :param stat: The Stat whose stage should be read
    :return: The stat stage for the relevant stat.
    """
    match stat:
        case Stat.ATTACK:
            return stages.attack
        case Stat.DEFENSE:
            return stages.defense
        case Stat.SP_ATTACK:
            return stages.sp_attack
        case Stat.SP_DEFENSE:
            return stages.sp_defense
        case Stat.SPEED:
            return stages.speed
        case Stat.ACCURACY:
            return stages.accuracy
        case Stat.EVASION:
            return stages.evasion
        case _:
            raise ValueError(f"Unknown stat {stat}")


def set_stage(stages: StatStages, stat: Stat, new_stage: int) -> None:
    """
    Sets the stat stage specified in `stat`.

    :param stages: The StatStages object to modify.
    :param stat: The relevant Stat whose stage should be set.
    :param new_stage: The new stat stage number to set.
    :return: Nothing.
    """
    if not MIN_STAGE <= new_stage <= MAX_STAGE:
        raise ValueError(
            f"New stage {new_stage} is out of range {MIN_STAGE} to {MAX_STAGE}"
        )
    match stat:
        case Stat.ATTACK:
            stages.attack = new_stage
        case Stat.DEFENSE:
            stages.defense = new_stage
        case Stat.SP_ATTACK:
            stages.sp_attack = new_stage
        case Stat.SP_DEFENSE:
            stages.sp_defense = new_stage
        case Stat.SPEED:
            stages.speed = new_stage
        case Stat.ACCURACY:
            stages.accuracy = new_stage
        case Stat.EVASION:
            stages.evasion = new_stage
        case _:
            raise ValueError(f"Unknown stat {stat}")


def modify_stage(
    stages: StatStages,
    stat: Stat,
    amount: int,
) -> int:
    """
    Modifies the stat stage specified in `stat` by the amount specified in `amount`, but clamps the stat stage between
    the maximum and minimum stage values.

    :param stages: The StatStages object to search through.
    :param stat: The stat whose stage should be modified.
    :param amount: The amount to modify the stat stage by.
    :return: The actual modification applied to the stat stage.
    """

    old_stage = get_stage(stages, stat)

    requested_stage = old_stage + amount

    clamped_stage = max(
        MIN_STAGE,
        min(MAX_STAGE, requested_stage),
    )

    set_stage(stages, stat, clamped_stage)

    return clamped_stage - old_stage


def stage_multiplier(
    stat: Stat,
    stage: int,
) -> float:
    """
    Calculates and returns the multiplier for the relevant stat given the stage of that stat.

    :param stat: The Stat object to calculate the multiplier for.
    :param stage: The stat stage for the relevant stat.
    :return: The multiplier for the relevant stat.
    """
    if not MIN_STAGE <= stage <= MAX_STAGE:
        raise ValueError(f"Illegal stat stage: {stage}")
    base = stat.stage_base
    if stage >= 0:
        return (base + stage) / base
    return base / (base - stage)
