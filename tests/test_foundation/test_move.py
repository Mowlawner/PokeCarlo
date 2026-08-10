from dataclasses import FrozenInstanceError

import pytest

from battle.battle_context import BattleContext
from battle.stub_rng import StubRNG
from move import Move, MoveCategory, MoveTarget
from move_effects.damage_effect import DamageEffect
from move_effects.move_effect import MoveEffectResult
from move_effects.stat_change_effect import StatChangeEffect
from pokemon_types import Type
from stats.stat import Stat


def test_move_can_be_created():
    move = Move(
        name="Earthquake",
        display_name="Earthquake",
        id=89,
        accuracy=100,
        pp=10,
        power=100,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=100),),
        move_flags=(),
    )

    assert move.name == "Earthquake"
    assert move.effects[0].power == 100
    assert move.move_type == Type.GROUND


def test_move_can_have_no_accuracy():
    move = Move(
        name="Aerial Ace",
        display_name="Aerial Ace",
        id=332,
        accuracy=None,
        pp=20,
        power=60,
        move_type=Type.FLYING,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=60),),
        move_flags=(),
    )

    assert move.accuracy is None


def test_move_is_immutable():
    move = Move(
        name="Tackle",
        display_name="Tackle",
        id=33,
        accuracy=100,
        pp=35,
        power=40,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=40),),
        move_flags=(),
    )

    with pytest.raises(FrozenInstanceError):
        move.effects[0].power = 50


def test_negative_power_raises():
    with pytest.raises(ValueError):
        Move(
            name="Bad Move",
            display_name="Bad Move",
            id=0,
            accuracy=100,
            pp=1,
            power=-1,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect(power=-1),),
            move_flags=(),
        )


def test_accuracy_above_100_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible",
            display_name="Impossible",
            id=0,
            accuracy=101,
            pp=1,
            power=50,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect(power=50),),
            move_flags=(),
        )


def test_zero_accuracy_raises():
    with pytest.raises(ValueError):
        Move(
            name="Broken",
            display_name="Broken",
            id=0,
            accuracy=0,
            pp=1,
            power=50,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect(power=50),),
            move_flags=(),
        )


def test_negative_accuracy_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible",
            display_name="Impossible",
            id=0,
            accuracy=-1,
            pp=1,
            power=50,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect(power=50),),
            move_flags=(),
        )


def test_non_default_priority_is_allowed():
    move = Move(
        name="Quick Attack",
        display_name="Quick Attack",
        id=98,
        accuracy=100,
        pp=30,
        power=40,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        priority=1,
        effects=(DamageEffect(power=40),),
        move_flags=(),
    )
    assert move.priority == 1


def test_invalid_priority_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible Priority",
            display_name="Impossible Priority",
            id=0,
            accuracy=100,
            pp=1,
            power=1,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            priority=6,
            effects=(DamageEffect(power=1),),
            move_flags=(),
        )


def test_priority_defaults_to_zero():
    move = Move(
        name="Tackle",
        display_name="Tackle",
        id=33,
        accuracy=100,
        pp=35,
        power=40,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=40),),
        move_flags=(),
    )

    assert move.priority == 0


def test_move_category_is_enum():
    move = Move(
        name="Swords Dance",
        display_name="Swords Dance",
        id=14,
        accuracy=None,
        pp=20,
        power=None,
        move_type=Type.NORMAL,
        category=MoveCategory.STATUS,
        effects=(
            StatChangeEffect(
                stat=Stat.ATTACK,
                stages=2,
            ),
        ),
        move_flags=(),
    )

    assert move.category == MoveCategory.STATUS


def test_status_move_cannot_have_damage_effect():
    with pytest.raises(ValueError):
        Move(
            name="Fake Damage Status",
            display_name="Fake Damage Status",
            id=0,
            accuracy=None,
            pp=1,
            power=None,
            move_type=Type.NORMAL,
            category=MoveCategory.STATUS,
            effects=(DamageEffect(power=0),),
            move_flags=(),
        )


def test_move_has_targeting_type():
    move = Move(
        name="Earthquake",
        display_name="Earthquake",
        id=89,
        accuracy=100,
        pp=10,
        power=100,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=100),),
        move_flags=(),
        targeting=MoveTarget.ALL_OTHERS,
    )

    assert move.targeting is MoveTarget.ALL_OTHERS


def test_targeting_defaults_to_single_target():
    move = Move(
        name="Dragon Claw",
        display_name="Dragon Claw",
        id=337,
        accuracy=100,
        pp=15,
        power=80,
        move_type=Type.DRAGON,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=80),),
        move_flags=(),
    )

    assert move.targeting is MoveTarget.SINGLE_TARGET


def test_move_can_have_multiple_effects():
    move = Move(
        name="Dragon Claw",
        display_name="Dragon Claw",
        id=337,
        accuracy=100,
        pp=15,
        power=80,
        move_type=Type.DRAGON,
        category=MoveCategory.PHYSICAL,
        effects=(
            DamageEffect(power=80),
            StatChangeEffect(
                stat=Stat.ATTACK,
                stages=1,
            ),
        ),
        move_flags=(),
    )

    assert len(move.effects) == 2
    assert isinstance(move.effects[0], DamageEffect)
    assert isinstance(move.effects[1], StatChangeEffect)


def test_move_passes_prior_effect_results_in_order(garchomp, battle_context):
    received_prior_results = []

    class RecordingEffect:
        def __init__(self, result):
            self.result = result

        def apply(
            self,
            *,
            user,
            targets,
            move_context,
            battle_context,
            prior_results=(),
        ):
            received_prior_results.append(prior_results)
            return self.result

    first_result = MoveEffectResult(applied=True)
    second_result = MoveEffectResult(applied=False)
    move = Move(
        name="TEST_MOVE",
        display_name="Test Move",
        id=9999,
        accuracy=None,
        pp=1,
        power=None,
        move_type=Type.NORMAL,
        category=MoveCategory.STATUS,
        effects=(RecordingEffect(first_result), RecordingEffect(second_result)),
        move_flags=(),
    )

    result = move.apply(user=garchomp, targets=(garchomp,), battle_context=battle_context)

    assert received_prior_results == [(), (first_result,)]
    assert result.effect_results == (first_result, second_result)


def test_move_apply_executes_damage_effect(
    garchomp,
    opponent_garchomp,
    earthquake,
    battle_context,
):
    starting_hp = opponent_garchomp.current_hp

    earthquake.apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        battle_context=battle_context,
    )

    assert opponent_garchomp.current_hp < starting_hp


def test_move_apply_returns_effect_results_for_swords_dance(
    garchomp, swords_dance, battle_context
):
    result = swords_dance.apply(
        user=garchomp,
        targets=(garchomp,),
        battle_context=battle_context,
    )

    assert result.applied
    assert result.effect_results[0].stat_stage_changes[0].amount == 2
    assert garchomp.stat_stages.attack == 2
    assert garchomp.current_hp == garchomp.stats.hp


def test_move_apply_accuracy_failure_skips_stat_change(
    garchomp, swords_dance, battle_state
):
    rng = StubRNG(accuracy_rolls=[0.99])
    inaccurate_swords_dance = Move(
        name=swords_dance.name,
        display_name=swords_dance.display_name,
        id=swords_dance.id,
        accuracy=50,
        pp=swords_dance.pp,
        power=swords_dance.power,
        move_type=swords_dance.move_type,
        category=swords_dance.category,
        effects=swords_dance.effects,
        move_flags=swords_dance.move_flags,
        targeting=swords_dance.targeting,
        priority=swords_dance.priority,
    )

    result = inaccurate_swords_dance.apply(
        user=garchomp,
        targets=(garchomp,),
        battle_context=BattleContext(battle_state, rng),
    )

    assert not result.applied
    assert garchomp.stat_stages.attack == 0


def test_move_applies_effect_when_accuracy_check_succeeds(
    garchomp,
    opponent_garchomp,
    earthquake,
    battle_state,
):
    rng = StubRNG(accuracy_rolls=[0.0])

    starting_hp = opponent_garchomp.current_hp

    earthquake.apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        battle_context=BattleContext(battle_state, rng),
    )

    assert opponent_garchomp.current_hp < starting_hp


def test_move_does_not_apply_effect_when_accuracy_check_fails(
    garchomp,
    opponent_garchomp,
    high_horsepower,
    battle_state,
):
    rng = StubRNG(accuracy_rolls=[0.99])

    starting_hp = opponent_garchomp.current_hp

    high_horsepower.apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        battle_context=BattleContext(battle_state, rng),
    )

    assert opponent_garchomp.current_hp == starting_hp


def test_perfect_accuracy_move_hits_on_max_roll(
    garchomp,
    opponent_garchomp,
    earthquake,
    battle_state,
):
    rng = StubRNG(accuracy_rolls=[0.99])

    starting_hp = opponent_garchomp.current_hp

    earthquake.apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        battle_context=BattleContext(battle_state, rng),
    )

    assert opponent_garchomp.current_hp < starting_hp


def test_move_checks_accuracy_independently_for_each_target(
    garchomp,
    opponent_garchomp,
    second_opponent_garchomp,
    rock_slide,
    battle_state,
):
    rng = StubRNG(
        accuracy_rolls=[
            0.0,  # first target hits
            0.99,  # second target misses
        ]
    )

    first_starting_hp = opponent_garchomp.current_hp
    second_starting_hp = second_opponent_garchomp.current_hp

    rock_slide.apply(
        user=garchomp,
        targets=(
            opponent_garchomp,
            second_opponent_garchomp,
        ),
        battle_context=BattleContext(
            battle_state,
            rng,
        ),
    )

    assert opponent_garchomp.current_hp < first_starting_hp
    assert second_opponent_garchomp.current_hp == second_starting_hp


def test_damage_roll_is_generated_for_each_target(
    garchomp,
    opponent_garchomp,
    second_opponent_garchomp,
    rock_slide,
    battle_state,
):
    rng = StubRNG(
        accuracy_rolls=[0.0, 0.0],
        damage_rolls=[0.85, 0.99],
        critical_rolls=[0.99, 0.99],
    )

    starting_hp_1 = opponent_garchomp.current_hp
    starting_hp_2 = second_opponent_garchomp.current_hp

    rock_slide.apply(
        user=garchomp,
        targets=(opponent_garchomp, second_opponent_garchomp),
        battle_context=BattleContext(battle_state, rng),
    )

    assert opponent_garchomp.current_hp < starting_hp_1
    assert second_opponent_garchomp.current_hp < starting_hp_2

    assert rng._damage_rolls == []
