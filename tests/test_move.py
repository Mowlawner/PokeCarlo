from dataclasses import FrozenInstanceError

import pytest

from move.move import Move, MoveCategory
from move_effects.damage_effect import DamageEffect
from move_effects.stat_change_effect import StatChangeEffect
from pokemon_types import Type
from stats.stat import Stat


def test_move_can_be_created():
    move = Move(
        name="Earthquake",
        power=100,
        accuracy=100,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect,),
    )

    assert move.name == "Earthquake"
    assert move.power == 100
    assert move.move_type == Type.GROUND


def test_move_can_have_no_accuracy():
    move = Move(
        name="Aerial Ace",
        power=60,
        accuracy=None,
        move_type=Type.FLYING,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect,),
    )

    assert move.accuracy is None


def test_move_is_immutable():
    move = Move(
        name="Tackle",
        power=40,
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect,),
    )

    with pytest.raises(FrozenInstanceError):
        move.power = 50


def test_negative_power_raises():
    with pytest.raises(ValueError):
        Move(
            name="Bad Move",
            power=-1,
            accuracy=100,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect,),
        )


def test_accuracy_above_100_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible",
            power=50,
            accuracy=101,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect,),
        )


def test_zero_accuracy_raises():
    with pytest.raises(ValueError):
        Move(
            name="Broken",
            power=50,
            accuracy=0,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect,),
        )


def test_negative_accuracy_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible",
            power=50,
            accuracy=-1,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            effects=(DamageEffect,),
        )


def test_non_default_priority_is_allowed():
    move = Move(
        name="Quick Attack",
        power=40,
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        priority=1,
        effects=(DamageEffect,),
    )
    assert move.priority == 1


def test_invalid_priority_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible Priority",
            power=1,
            accuracy=100,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
            priority=6,
            effects=(DamageEffect,),
        )


def test_priority_defaults_to_zero():
    move = Move(
        name="Tackle",
        power=40,
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect,),
    )

    assert move.priority == 0


def test_move_category_is_enum():
    move = Move(
        name="Swords Dance",
        power=0,
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
