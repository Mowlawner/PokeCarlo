import pytest

from move import Move, MoveCategory
from move_effects.damage_effect import DamageEffect
from move_effects.stat_change_effect import StatChangeEffect
from pokemon_set import PokemonSet
from pokemon_species import PokemonSpecies
from pokemon_types import Type
from stats.base_stats import BaseStats
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature
from stats.stat import Stat


@pytest.fixture
def tackle() -> Move:
    return Move(
        name="Tackle",
        power=40,
        accuracy=100,
        move_type=Type.NORMAL,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(),),
    )


@pytest.fixture
def earthquake() -> Move:
    return Move(
        name="Earthquake",
        power=100,
        accuracy=100,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(),),
    )


@pytest.fixture
def dragon_claw() -> Move:
    return Move(
        name="Dragon Claw",
        power=80,
        accuracy=100,
        move_type=Type.DRAGON,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(),),
    )


@pytest.fixture
def swords_dance() -> Move:
    return Move(
        name="Swords Dance",
        power=0,
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
        power=95,
        accuracy=95,
        move_type=Type.GROUND,
        category=MoveCategory.PHYSICAL,
        effects=(DamageEffect(),),
    )


@pytest.fixture
def garchomp_species() -> PokemonSpecies:
    return PokemonSpecies(
        name="Garchomp",
        types=(Type.DRAGON, Type.GROUND),
        base_stats=BaseStats(
            hp=108,
            attack=130,
            defense=95,
            sp_attack=80,
            sp_defense=85,
            speed=102,
        ),
    )


@pytest.fixture
def garchomp_set(
    garchomp_species: PokemonSpecies,
    tackle: Move,
) -> PokemonSet:
    return PokemonSet(
        species=garchomp_species,
        level=50,
        nature=Nature.JOLLY,
        ivs=IVs(
            hp=31,
            attack=31,
            defense=31,
            sp_attack=31,
            sp_defense=31,
            speed=31,
        ),
        evs=EVs(
            hp=4,
            attack=252,
            defense=0,
            sp_attack=0,
            sp_defense=0,
            speed=252,
        ),
        moves=(tackle,),
    )
