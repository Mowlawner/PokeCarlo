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
        name="TACKLE",
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


@pytest.fixture
def earthquake() -> Move:
    return Move(
        name="EARTHQUAKE",
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


@pytest.fixture
def dragon_claw() -> Move:
    return Move(
        name="DRAGON_CLAW",
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


@pytest.fixture
def rock_slide() -> Move:
    return Move(
        name="ROCK_SLIDE",
        display_name="Rock Slide",
        id=157,
        accuracy=90,
        pp=10,
        power=75,
        move_type=Type.ROCK,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=75),),
        move_flags=(),
        targeting=MoveTarget.ALL_OPPONENTS,
    )


@pytest.fixture
def swords_dance() -> Move:
    return Move(
        name="SWORDS_DANCE",
        display_name="Swords Dance",
        id=14,
        accuracy=None,  # or however you decide to represent "never misses"
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


@pytest.fixture
def high_horsepower() -> Move:
    return Move(
        name="HIGH_HORSEPOWER",
        display_name="High Horsepower",
        id=667,
        accuracy=95,
        pp=10,
        power=95,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(power=95),),
        move_flags=(),
    )


@pytest.fixture
def protect():
    return Move(
        name="PROTECT",
        display_name="Protect",
        id=182,
        accuracy=None,
        pp=10,
        power=None,
        move_type=Type.NORMAL,
        category=MoveCategory.STATUS,
        effects=(),
        move_flags=(),
        targeting=MoveTarget.SELF,
        priority=4,
    )
