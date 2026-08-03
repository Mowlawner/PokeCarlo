from dataclasses import FrozenInstanceError

import pytest

from move import Move, MoveCategory
from pokemon_types import Type


def test_move_can_be_created():
    move = Move(
        name="Earthquake",
        power=100,
        accuracy=100,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
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
    )

    assert move.accuracy is None


def test_move_is_immutable():
    move = Move(
        name="Tackle",
        power=40,
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
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
        )


def test_accuracy_above_100_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible",
            power=50,
            accuracy=101,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
        )


def test_zero_accuracy_raises():
    with pytest.raises(ValueError):
        Move(
            name="Broken",
            power=50,
            accuracy=0,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
        )


def test_negative_accuracy_raises():
    with pytest.raises(ValueError):
        Move(
            name="Impossible",
            power=50,
            accuracy=-1,
            move_type=Type.NORMAL,
            category=MoveCategory.PHYSICAL,
        )


def test_non_default_priority_is_allowed():
    move = Move(
        name="Quick Attack",
        power=40,
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        priority=1,
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
        )


def test_priority_defaults_to_zero():
    move = Move(
        name="Tackle",
        power=40,
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
    )

    assert move.priority == 0


def test_move_category_is_enum():
    move = Move(
        name="Swords Dance",
        power=0,
        accuracy=None,
        move_type=Type.NORMAL,
        category=MoveCategory.STATUS,
    )

    assert move.category == MoveCategory.STATUS
