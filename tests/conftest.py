import pytest

from battle import BattleState
from battle.battle_context import BattleContext
from battle.battle_resolver import BattleResolver
from battle.rng import RNG
from move import Move, MoveCategory, MoveTarget
from move_effects.damage_effect import DamageEffect
from move_effects.stat_change_effect import StatChangeEffect
from pokemon import Pokemon
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


@pytest.fixture
def jolly_garchomp_set(
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


@pytest.fixture
def adamant_garchomp_set(
    garchomp_species: PokemonSpecies,
    tackle: Move,
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
    )


@pytest.fixture
def garchomp(
    jolly_garchomp_set: PokemonSet,
) -> Pokemon:
    return Pokemon.from_set(jolly_garchomp_set)


@pytest.fixture
def battle_state(
    garchomp,
    ally_garchomp,
    opponent_garchomp,
    second_opponent_garchomp,
) -> BattleState:
    return BattleState(
        player_active=(
            garchomp,
            ally_garchomp,
        ),
        opponent_active=(
            opponent_garchomp,
            second_opponent_garchomp,
        ),
    )


@pytest.fixture
def battle_context(battle_state: BattleState) -> BattleContext:
    return BattleContext(battle_state, rng=RNG(42))


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


@pytest.fixture
def battle_resolver(battle_context) -> BattleResolver:
    return BattleResolver(battle_context)
