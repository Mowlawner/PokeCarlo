from dataclasses import FrozenInstanceError

import pytest

from move.move_context import MoveContext
from move_effects.stat_change_effect import StatChangeEffect
from pokemon import Pokemon
from stats.stat import Stat
from stats.stat_utils import modify_stage


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

    result = effect.apply(
        user=pokemon,
        targets=(pokemon,),
        move_context=move_context,
        battle_context=battle_context,
    )

    assert pokemon.stat_stages.attack == 2
    assert result.applied
    assert result.stat_stage_changes[0].amount == 2


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

    result = effect.apply(
        user=first,
        targets=(first, second),
        move_context=move_context,
        battle_context=battle_context,
    )

    assert first.stat_stages.defense == -1
    assert second.stat_stages.defense == -1
    assert result.applied
    assert [change.amount for change in result.stat_stage_changes] == [-1, -1]


def test_stat_change_effect_reports_no_change_at_stage_limit(
    jolly_garchomp_set, swords_dance, battle_context
):
    pokemon = Pokemon.from_set(jolly_garchomp_set)
    modify_stage(pokemon.stat_stages, Stat.ATTACK, 6)

    result = StatChangeEffect(stat=Stat.ATTACK, stages=2).apply(
        user=pokemon,
        targets=(pokemon,),
        move_context=MoveContext(swords_dance.move_type, swords_dance.category),
        battle_context=battle_context,
    )

    assert pokemon.stat_stages.attack == 6
    assert not result.applied
    assert result.stat_stage_changes == ()


def test_stat_change_effect_respects_negative_stage_limit(
    jolly_garchomp_set, swords_dance, battle_context
):
    pokemon = Pokemon.from_set(jolly_garchomp_set)
    modify_stage(pokemon.stat_stages, Stat.ATTACK, -6)

    result = StatChangeEffect(stat=Stat.ATTACK, stages=-1).apply(
        user=pokemon,
        targets=(pokemon,),
        move_context=MoveContext(swords_dance.move_type, swords_dance.category),
        battle_context=battle_context,
    )

    assert pokemon.stat_stages.attack == -6
    assert not result.applied


def test_stat_change_effect_is_immutable():
    effect = StatChangeEffect(stat=Stat.ATTACK, stages=2)

    with pytest.raises(FrozenInstanceError):
        effect.stages = 1


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
