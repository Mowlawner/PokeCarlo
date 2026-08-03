import pytest

from move_effects.stat_change_effect import StatChangeEffect
from pokemon import Pokemon
from stats.stat import Stat


def test_stat_change_effect_applies_to_target(jolly_garchomp_set):
    pokemon = Pokemon.from_set(jolly_garchomp_set)

    effect = StatChangeEffect(
        stat=Stat.ATTACK,
        stages=2,
    )

    effect.apply(
        user=pokemon,
        targets=(pokemon,),
    )

    assert pokemon.stat_stages.attack == 2


def test_stat_change_effect_applies_to_multiple_targets(jolly_garchomp_set):
    first = Pokemon.from_set(jolly_garchomp_set)
    second = Pokemon.from_set(jolly_garchomp_set)

    effect = StatChangeEffect(
        stat=Stat.DEFENSE,
        stages=-1,
    )

    effect.apply(
        user=first,
        targets=(first, second),
    )

    assert first.stat_stages.defense == -1
    assert second.stat_stages.defense == -1


def test_zero_stage_change_is_invalid():
    with pytest.raises(ValueError):
        StatChangeEffect(
            stat=Stat.ATTACK,
            stages=0,
        )


def test_stage_change_cannot_exceed_six():
    with pytest.raises(ValueError):
        StatChangeEffect(
            stat=Stat.ATTACK,
            stages=7,
        )


def test_stage_change_cannot_be_less_than_negative_six():
    with pytest.raises(ValueError):
        StatChangeEffect(
            stat=Stat.ATTACK,
            stages=-7,
        )
