import pytest

from stats.stat import Stat
from stats.stat_stages import StatStages
from stats.stat_utils import modify_stage, set_stage


def test_modify_stage_simple():
    stages = StatStages()

    delta = modify_stage(
        stages,
        Stat.ATTACK,
        2,
    )

    assert delta == 2
    assert stages.attack == 2


def test_modify_stage_clamps_up():
    stages = StatStages(attack=5)

    delta = modify_stage(
        stages,
        Stat.ATTACK,
        2,
    )

    assert delta == 1
    assert stages.attack == 6


def test_modify_stage_already_max():
    stages = StatStages(attack=6)

    delta = modify_stage(
        stages,
        Stat.ATTACK,
        2,
    )

    assert delta == 0
    assert stages.attack == 6


def test_modify_stage_clamps_down():
    stages = StatStages(speed=-5)

    delta = modify_stage(
        stages,
        Stat.SPEED,
        -2,
    )

    assert delta == -1
    assert stages.speed == -6


def test_modify_stage_already_min():
    stages = StatStages(speed=-6)

    delta = modify_stage(
        stages,
        Stat.SPEED,
        -2,
    )

    assert delta == 0
    assert stages.speed == -6


def test_set_stage_rejects_large_stage():
    stages = StatStages()

    with pytest.raises(ValueError):
        set_stage(
            stages,
            Stat.ATTACK,
            7,
        )


def test_set_stage_rejects_small_stage():
    stages = StatStages()

    with pytest.raises(ValueError):
        set_stage(
            stages,
            Stat.ATTACK,
            -7,
        )


def test_stats_get_attack(garchomp):
    assert garchomp.stats.get(Stat.ATTACK) == garchomp.stats.attack


def test_stats_get_special_defense(garchomp):
    assert garchomp.stats.get(Stat.SP_DEFENSE) == garchomp.stats.sp_defense
