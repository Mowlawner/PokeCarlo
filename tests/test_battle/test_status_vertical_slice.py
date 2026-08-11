import json

from ability import Ability
from battle import BattleContext, BattleResolver, BattleState, StubRNG
from battle.action import MoveAction
from battle.decision.legal_actions import get_legal_actions
from database.ability_database import AbilityDatabase
from database.item_database import ItemDatabase
from database.learnset_database import LearnsetDatabase
from database.move_database import MoveDatabase
from database.species_database import SpeciesDatabase
from move_effects.move_effect import StatusApplicationOutcome
from pokemon import Pokemon
from pokemon_set_resolver import PokemonSetResolver
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature
from status_condition import StatusCondition


def make_thunder_wave_resolver(tmp_path, garchomp_species):
    move_directory = tmp_path / "moves"
    move_directory.mkdir()
    (move_directory / "thunder-wave.json").write_text(
        json.dumps(
            {
                "accuracy": 90,
                "category": "STATUS",
                "display_name": "Thunder Wave",
                "effects": [{"type": "status", "status": "PARALYSIS"}],
                "id": 86,
                "move_flags": [],
                "move_name": "THUNDER_WAVE",
                "move_type": "ELECTRIC",
                "power": None,
                "pp": 20,
                "priority": 0,
                "target": "SINGLE_TARGET",
            }
        ),
        encoding="utf-8",
    )

    return PokemonSetResolver(
        species_database=SpeciesDatabase({garchomp_species.name: garchomp_species}),
        ability_database=AbilityDatabase(
            {
                "ROUGH_SKIN": Ability(
                    name="ROUGH_SKIN",
                    display_name="Rough Skin",
                    id=17,
                    generation="GENERATION_III",
                )
            }
        ),
        move_database=MoveDatabase.load(move_directory),
        item_database=ItemDatabase({}),
        learnset_database=LearnsetDatabase(
            {garchomp_species.name: frozenset({"THUNDER_WAVE"})}
        ),
    )


def make_flamethrower_resolver(tmp_path, garchomp_species):
    move_directory = tmp_path / "flamethrower-moves"
    move_directory.mkdir()
    (move_directory / "flamethrower.json").write_text(
        json.dumps(
            {
                "accuracy": 100,
                "category": "SPECIAL",
                "display_name": "Flamethrower",
                "effects": [
                    {"type": "damage", "power": 90},
                    {"type": "status", "status": "BURN", "chance": 10},
                ],
                "id": 53,
                "move_flags": [],
                "move_name": "FLAMETHROWER",
                "move_type": "FIRE",
                "power": 90,
                "pp": 15,
                "priority": 0,
                "target": "SINGLE_TARGET",
            }
        ),
        encoding="utf-8",
    )
    return PokemonSetResolver(
        species_database=SpeciesDatabase({garchomp_species.name: garchomp_species}),
        ability_database=AbilityDatabase(
            {"ROUGH_SKIN": Ability("ROUGH_SKIN", "Rough Skin", 17, "GENERATION_III")}
        ),
        move_database=MoveDatabase.load(move_directory),
        item_database=ItemDatabase({}),
        learnset_database=LearnsetDatabase(
            {garchomp_species.name: frozenset({"FLAMETHROWER"})}
        ),
    )


def make_battlers(resolver, garchomp_species):
    def resolve_pokemon():
        pokemon_set = resolver.resolve(
            species_name=garchomp_species.name,
            ability_name="ROUGH_SKIN",
            move_names=("THUNDER_WAVE",),
            level=50,
            nature=Nature.JOLLY,
            ivs=IVs(31, 31, 31, 31, 31, 31),
            evs=EVs(6, 252, 0, 0, 0, 252),
        )
        return Pokemon.from_set(pokemon_set)

    return resolve_pokemon(), resolve_pokemon()


def resolve_thunder_wave(
    *, tmp_path, garchomp_species, rng, initial_status=StatusCondition.NONE
):
    resolver = make_thunder_wave_resolver(tmp_path, garchomp_species)
    attacker, target = make_battlers(resolver, garchomp_species)
    target.status = initial_status
    context = BattleContext(
        state=BattleState(player_active=(attacker,), opponent_active=(target,)),
        rng=rng,
    )
    action = next(
        action
        for action in get_legal_actions(battle_context=context, pokemon=attacker)
        if isinstance(action, MoveAction)
    )
    result = BattleResolver(context).resolve_turn(actions=(action,))[0][1]
    return target, result


def test_database_thunder_wave_paralyzes_through_battle_resolution(
    tmp_path, garchomp_species
):
    target, result = resolve_thunder_wave(
        tmp_path=tmp_path,
        garchomp_species=garchomp_species,
        rng=StubRNG(accuracy_rolls=[0.0]),
    )

    assert target.status is StatusCondition.PARALYSIS
    assert result is not None
    assert (
        result.effect_results[0].status_applications[0].outcome
        is StatusApplicationOutcome.APPLIED
    )


def test_thunder_wave_does_not_overwrite_existing_status(tmp_path, garchomp_species):
    target, result = resolve_thunder_wave(
        tmp_path=tmp_path,
        garchomp_species=garchomp_species,
        rng=StubRNG(accuracy_rolls=[0.0]),
        initial_status=StatusCondition.BURN,
    )

    assert target.status is StatusCondition.BURN
    assert not result.effect_results[0].applied
    assert (
        result.effect_results[0].status_applications[0].outcome
        is StatusApplicationOutcome.ALREADY_AFFECTED_BY_OTHER_STATUS
    )


def test_thunder_wave_rejects_existing_paralysis_without_mutation(
    tmp_path, garchomp_species
):
    target, result = resolve_thunder_wave(
        tmp_path=tmp_path,
        garchomp_species=garchomp_species,
        rng=StubRNG(accuracy_rolls=[0.0]),
        initial_status=StatusCondition.PARALYSIS,
    )

    assert target.status is StatusCondition.PARALYSIS
    assert not result.effect_results[0].applied
    assert (
        result.effect_results[0].status_applications[0].outcome
        is StatusApplicationOutcome.ALREADY_AFFECTED
    )


def test_thunder_wave_miss_does_not_apply_paralysis(tmp_path, garchomp_species):
    target, result = resolve_thunder_wave(
        tmp_path=tmp_path,
        garchomp_species=garchomp_species,
        rng=StubRNG(accuracy_rolls=[0.99]),
    )

    assert target.status is StatusCondition.NONE
    assert result is not None
    assert result.effect_results[0].status_applications == ()
    assert not result.effect_results[0].applied


def test_database_flamethrower_executes_damage_then_independent_burn(
    tmp_path, garchomp_species
):
    resolver = make_flamethrower_resolver(tmp_path, garchomp_species)
    attacker_set = resolver.resolve(
        species_name=garchomp_species.name,
        ability_name="ROUGH_SKIN",
        move_names=("FLAMETHROWER",),
        level=50,
        nature=Nature.JOLLY,
        ivs=IVs(31, 31, 31, 31, 31, 31),
        evs=EVs(6, 252, 0, 0, 0, 252),
    )
    target_set = resolver.resolve(
        species_name=garchomp_species.name,
        ability_name="ROUGH_SKIN",
        move_names=("FLAMETHROWER",),
        level=50,
        nature=Nature.JOLLY,
        ivs=IVs(31, 31, 31, 31, 31, 31),
        evs=EVs(6, 252, 0, 0, 0, 252),
    )
    attacker, target = Pokemon.from_set(attacker_set), Pokemon.from_set(target_set)
    context = BattleContext(
        state=BattleState(player_active=(attacker,), opponent_active=(target,)),
        rng=StubRNG(
            accuracy_rolls=[0.0],
            critical_rolls=[1.0],
            damage_rolls=[1.0],
            rolls=[0.0],
        ),
    )
    action = MoveAction(attacker, attacker.pokemon_set.moves[0], target)

    result = BattleResolver(context).resolve_turn((action,))[0][1]

    assert result is not None
    assert len(result.effect_results) == 2
    assert result.effect_results[0].damage_dealt[0].amount > 0
    assert target.status is StatusCondition.BURN
