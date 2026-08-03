from dataclasses import FrozenInstanceError

import pytest

from move import Move, MoveCategory, MoveTarget
from move_effects.damage_effect import DamageEffect
from move_effects.stat_change_effect import StatChangeEffect
from pokemon_types import Type
from stats.stat import Stat


def test_move_can_be_created():
    move = Move(
        name="Earthquake",
        accuracy=100,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=100),),
    )

    assert move.name == "Earthquake"
    assert move.effects[0].power == 100
    assert move.move_type == Type.GROUND


def test_move_can_have_no_accuracy():
    move = Move(
        name="Aerial Ace",
        accuracy=None,
        move_type=Type.FLYING,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=60),),
    )

    assert move.accuracy is None


def test_move_is_immutable():
    move = Move(
        name="Tackle",
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=40),),
    )

    with pytest.raises(FrozenInstanceError):
        move.effects[0].power = 50


def test_negative_power_raises():
    with pytest.raises(ValueError):
        Move(
            name="Bad Move",
            accuracy=100,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect(power=-1),),
        )


def test_accuracy_above_100_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible",
            accuracy=101,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect(power=50),),
        )


def test_zero_accuracy_raises():
    with pytest.raises(ValueError):
        Move(
            name="Broken",
            accuracy=0,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect(power=50),),
        )


def test_negative_accuracy_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible",
            accuracy=-1,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect(power=50),),
        )


def test_non_default_priority_is_allowed():
    move = Move(
        name="Quick Attack",
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        priority=1,
        effects=(DamageEffect(power=40),),
    )
    assert move.priority == 1


def test_invalid_priority_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible Priority",
            accuracy=100,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            priority=6,
            effects=(DamageEffect(power=1),),
        )


def test_priority_defaults_to_zero():
    move = Move(
        name="Tackle",
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=40),),
    )

    assert move.priority == 0


def test_move_category_is_enum():
    move = Move(
        name="Swords Dance",
        accuracy=None,
        move_type=Type.NORMAL,
        category=MoveCategory.STATUS,
        effects=(
            StatChangeEffect(
                stat=Stat.ATTACK,
                stages=2,
            ),
        ),
    )

    assert move.category == MoveCategory.STATUS


def test_status_move_cannot_have_damage_effect():
    with pytest.raises(ValueError):
        Move(
            name="Fake Damage Status",
            accuracy=None,
            move_type=Type.NORMAL,
            category=MoveCategory.STATUS,
            effects=(DamageEffect(power=0),),
        )


def test_move_has_targeting_type():
    move = Move(
        name="Earthquake",
        accuracy=100,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=100),),
        targeting=MoveTarget.ALL_OTHERS,
    )

    assert move.targeting is MoveTarget.ALL_OTHERS


def test_targeting_defaults_to_single_target():
    move = Move(
        name="Dragon Claw",
        accuracy=100,
        move_type=Type.DRAGON,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=80),),
    )

    assert move.targeting is MoveTarget.SINGLE_TARGET


def test_move_can_have_multiple_effects():
    move = Move(
        name="Dragon Claw",
        accuracy=100,
        move_type=Type.DRAGON,
        category=MoveCategory.PHYSICAL,
        effects=(
            DamageEffect(power=80),
            StatChangeEffect(
                stat=Stat.ATTACK,
                stages=1,
            ),
        ),
    )

    assert len(move.effects) == 2
    assert isinstance(move.effects[0], DamageEffect)
    assert isinstance(move.effects[1], StatChangeEffect)
