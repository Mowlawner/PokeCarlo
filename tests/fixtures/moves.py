import pytest

from move import Move, MoveCategory, MoveTarget
from move.move_context import MoveContext
from move_effects.damage_effect import DamageEffect
from move_effects.stat_change_effect import StatChangeEffect
from pokemon_types import Type
from stats.stat import Stat


@pytest.fixture
def move_context_factory():
    def factory(
        move_type: Type,
        move_category: MoveCategory = MoveCategory.SPECIAL,
    ):
        return MoveContext(
            move_type=move_type,
            move_category=move_category,
        )

    return factory


@pytest.fixture
def tackle() -> Move:
    return Move(
        name="Tackle",
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=40),),
    )


@pytest.fixture
def earthquake() -> Move:
    return Move(
        name="Earthquake",
        accuracy=100,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=100),),
        targeting=MoveTarget.ALL_OTHERS,
    )


@pytest.fixture
def dragon_claw() -> Move:
    return Move(
        name="Dragon Claw",
        accuracy=100,
        move_type=Type.DRAGON,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=80),),
    )


@pytest.fixture
def rock_slide() -> Move:
    return Move(
        name="Rock Slide",
        accuracy=90,
        move_type=Type.ROCK,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=75),),
        targeting=MoveTarget.ALL_OPPONENTS,
    )


@pytest.fixture
def swords_dance() -> Move:
    return Move(
        name="Swords Dance",
        accuracy=None,  # or however you decide to represent "never misses"
        move_type=Type.NORMAL,
        category=MoveCategory.STATUS,
        effects=(
            StatChangeEffect(
                stat=Stat.ATTACK,
                stages=2,
            ),
        ),
    )


@pytest.fixture
def high_horsepower() -> Move:
    return Move(
        name="High Horsepower",
        accuracy=95,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=95),),
    )


@pytest.fixture
def protect():
    return Move(
        name="Protect",
        accuracy=None,
        move_type=Type.NORMAL,
        category=MoveCategory.STATUS,
        effects=(),
        targeting=MoveTarget.SELF,
        priority=4,
    )
