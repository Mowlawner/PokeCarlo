import pytest

from move import Move
from pokemon_set import PokemonSet
from pokemon_species import PokemonSpecies
from stats.base_stats import BaseStats
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature


@pytest.fixture
def tackle() -> Move:
    return Move(
        name="Tackle",
        power=40,
        accuracy=100,
        move_type="Normal",
        category="Physical",
    )


@pytest.fixture
def earthquake() -> Move:
    return Move(
        name="Earthquake",
        power=100,
        accuracy=100,
        move_type="Ground",
        category="Physical",
    )


@pytest.fixture
def dragon_claw() -> Move:
    return Move(
        name="Dragon Claw",
        power=80,
        accuracy=100,
        move_type="Dragon",
        category="Physical",
    )


@pytest.fixture
def swords_dance() -> Move:
    return Move(
        name="Swords Dance",
        power=0,
        accuracy=0,  # or however you decide to represent "never misses"
        move_type="Normal",
        category="Status",
    )


@pytest.fixture
def garchomp_species() -> PokemonSpecies:
    return PokemonSpecies(
        name="Garchomp",
        types=("Dragon", "Ground"),
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
