import pytest

from abilities.ability import Ability
from move import Move
from pokemon import Pokemon
from pokemon_set import PokemonSet
from pokemon_species import PokemonSpecies
from pokemon_types import Type
from stats.base_stats import BaseStats
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature


###SPECIES###
@pytest.fixture
def garchomp_species(rough_skin, sand_veil) -> PokemonSpecies:
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
        abilities=(rough_skin, sand_veil),
    )


@pytest.fixture
def gyarados_species(intimidate, moxie) -> PokemonSpecies:
    return PokemonSpecies(
        name="Gyarados",
        types=(Type.WATER, Type.FLYING),
        base_stats=BaseStats(
            hp=95,
            attack=125,
            defense=79,
            sp_attack=60,
            sp_defense=100,
            speed=81,
        ),
        abilities=(intimidate, moxie),
    )


@pytest.fixture
def tyranitar_species(sand_stream, unnerve) -> PokemonSpecies:
    return PokemonSpecies(
        name="Tyranitar",
        types=(
            Type.ROCK,
            Type.DARK,
        ),
        base_stats=BaseStats(
            hp=100,
            attack=134,
            defense=110,
            sp_attack=95,
            sp_defense=100,
            speed=61,
        ),
        abilities=(
            sand_stream,
            unnerve,
        ),
    )


###SET###


@pytest.fixture
def jolly_garchomp_set(
    garchomp_species: PokemonSpecies, tackle: Move, rough_skin: Ability
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
            hp=6,
            attack=252,
            defense=0,
            sp_attack=0,
            sp_defense=0,
            speed=252,
        ),
        moves=(tackle,),
        ability=rough_skin,
    )


@pytest.fixture
def jolly_gyarados_set(
    gyarados_species: PokemonSpecies, tackle: Move, intimidate: Ability
) -> PokemonSet:
    return PokemonSet(
        species=gyarados_species,
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
            defense=2,
            sp_attack=0,
            sp_defense=0,
            speed=252,
        ),
        moves=(tackle,),
        ability=intimidate,
    )


@pytest.fixture
def adamant_garchomp_set(
    garchomp_species: PokemonSpecies, tackle: Move, rough_skin: Ability
) -> PokemonSet:
    return PokemonSet(
        species=garchomp_species,
        level=50,
        nature=Nature.ADAMANT,
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
        ability=rough_skin,
    )


@pytest.fixture
def bulky_tyranitar_set(
    tyranitar_species,
    tackle,
):
    return PokemonSet(
        species=tyranitar_species,
        level=50,
        nature=Nature.ADAMANT,
        ivs=IVs(
            hp=31,
            attack=31,
            defense=31,
            sp_attack=31,
            sp_defense=31,
            speed=31,
        ),
        evs=EVs(
            hp=252,
            attack=252,
            defense=4,
            sp_attack=0,
            sp_defense=0,
            speed=0,
        ),
        moves=(tackle,),
        ability=tyranitar_species.abilities[0],
    )


###COMBATANTS###


@pytest.fixture
def garchomp(
    jolly_garchomp_set: PokemonSet,
) -> Pokemon:
    return Pokemon.from_set(jolly_garchomp_set)


@pytest.fixture
def gyarados(
    jolly_gyarados_set: PokemonSet,
) -> Pokemon:
    return Pokemon.from_set(jolly_gyarados_set)


@pytest.fixture
def tyranitar(
    bulky_tyranitar_set,
):
    return Pokemon.from_set(bulky_tyranitar_set)


@pytest.fixture
def opponent_garchomp(garchomp_species, jolly_garchomp_set) -> Pokemon:
    return Pokemon.from_set(jolly_garchomp_set)


@pytest.fixture
def adamant_garchomp(garchomp_species, adamant_garchomp_set) -> Pokemon:
    return Pokemon.from_set(adamant_garchomp_set)


@pytest.fixture
def ally_garchomp(garchomp_species, jolly_garchomp_set) -> Pokemon:
    return Pokemon.from_set(jolly_garchomp_set)


@pytest.fixture
def second_opponent_garchomp(jolly_garchomp_set) -> Pokemon:
    return Pokemon.from_set(jolly_garchomp_set)
