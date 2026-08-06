import pytest

from move.move_context import MoveContext
from move_effects.stat_change_effect import StatChangeEffect
from pokemon import Pokemon
from stats.stat import Stat


def test_stat_change_effect_applies_to_target(
    jolly_garchomp_set, swords_dance, battle_context
):
    pokemon = Pokemon.from_set(jolly_garchomp_set)

    effect = StatChangeEffect(
        stat=Stat.ATTACK,
        stages=2,
    )

    move_context = MoveContext(
        swords_dance.move_type, move_category=swords_dance.category
    )

    effect.apply(
        user=pokemon,
        targets=(pokemon,),
        move_context=move_context,
        battle_context=battle_context,
    )

    assert pokemon.stat_stages.attack == 2


def test_stat_change_effect_applies_to_multiple_targets(
    jolly_garchomp_set, swords_dance, battle_context
):
    first = Pokemon.from_set(jolly_garchomp_set)
    second = Pokemon.from_set(jolly_garchomp_set)

    move_context = MoveContext(swords_dance.move_type, swords_dance.category)

    effect = StatChangeEffect(
        stat=Stat.DEFENSE,
        stages=-1,
    )

    effect.apply(
        user=first,
        targets=(first, second),
        move_context=move_context,
        battle_context=battle_context,
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
