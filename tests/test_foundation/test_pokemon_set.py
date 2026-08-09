from dataclasses import FrozenInstanceError, fields, replace

import pytest

from ability import Ability
from pokemon import Pokemon
from pokemon_set import PokemonSet
from stats.stat_stages import StatStages


def test_one_move_is_allowed(jolly_garchomp_set):
    new_set = replace(jolly_garchomp_set, moves=jolly_garchomp_set.moves)

    assert len(new_set.moves) == 1


def test_four_moves_are_allowed(
    jolly_garchomp_set,
    tackle,
    earthquake,
    dragon_claw,
    swords_dance,
):
    moves = (
        tackle,
        earthquake,
        dragon_claw,
        swords_dance,
    )

    new_set = replace(jolly_garchomp_set, moves=moves)

    assert len(new_set.moves) == 4


def test_zero_moves_raises(jolly_garchomp_set):
    with pytest.raises(ValueError):
        replace(
            jolly_garchomp_set,
            moves=(),
        )


def test_five_moves_raises(
    jolly_garchomp_set, tackle, earthquake, dragon_claw, swords_dance, high_horsepower
):
    with pytest.raises(ValueError):
        replace(
            jolly_garchomp_set,
            moves=(
                tackle,
                earthquake,
                dragon_claw,
                swords_dance,
                high_horsepower,
            ),
        )


def test_from_set(jolly_garchomp_set):
    pokemon = Pokemon.from_set(jolly_garchomp_set)

    assert pokemon.pokemon_set is jolly_garchomp_set

    assert pokemon.current_hp == pokemon.stats.hp
    assert pokemon.stat_stages == StatStages()

    pokemon.current_hp = 0

    assert pokemon.is_fainted

    pokemon.current_hp = 1

    assert not pokemon.is_fainted


def test_duplicate_moves_raise(
    jolly_garchomp_set,
    tackle,
):
    with pytest.raises(ValueError):
        replace(
            jolly_garchomp_set,
            moves=(
                tackle,
                tackle,
            ),
        )


def test_valid_static_ability_and_learnset_move_are_accepted(
    jolly_garchomp_set,
    tackle,
):
    static_ability = Ability(
        name="ROUGH_SKIN",
        display_name="Rough Skin",
        id=17,
        generation="GENERATION_III",
    )

    configured_set = PokemonSet.from_components(
        species=jolly_garchomp_set.species,
        level=jolly_garchomp_set.level,
        nature=jolly_garchomp_set.nature,
        ivs=jolly_garchomp_set.ivs,
        evs=jolly_garchomp_set.evs,
        ability=static_ability,
        moves=(tackle,),
        learnset=frozenset({"TACKLE"}),
    )

    assert configured_set.ability is static_ability


def test_ability_not_in_species_is_rejected(jolly_garchomp_set):
    static_ability = Ability(
        name="INTIMIDATE",
        display_name="Intimidate",
        id=22,
        generation="GENERATION_III",
    )

    with pytest.raises(ValueError, match="not a valid ability"):
        PokemonSet.from_components(
            species=jolly_garchomp_set.species,
            level=jolly_garchomp_set.level,
            nature=jolly_garchomp_set.nature,
            ivs=jolly_garchomp_set.ivs,
            evs=jolly_garchomp_set.evs,
            moves=jolly_garchomp_set.moves,
            ability=static_ability,
            learnset=frozenset({"TACKLE"}),
        )


def test_move_not_in_learnset_is_rejected(jolly_garchomp_set, protect):
    with pytest.raises(ValueError, match="cannot learn: PROTECT"):
        PokemonSet.from_components(
            species=jolly_garchomp_set.species,
            level=jolly_garchomp_set.level,
            nature=jolly_garchomp_set.nature,
            ivs=jolly_garchomp_set.ivs,
            evs=jolly_garchomp_set.evs,
            moves=(protect,),
            ability=jolly_garchomp_set.ability,
            learnset=frozenset({"TACKLE"}),
        )


def test_four_distinct_moves_are_accepted(
    jolly_garchomp_set,
    tackle,
    earthquake,
    dragon_claw,
    swords_dance,
):
    configured_set = replace(
        jolly_garchomp_set,
        moves=(tackle, earthquake, dragon_claw, swords_dance),
    )

    assert len(configured_set.moves) == 4


def test_pokemon_set_does_not_store_learnset(jolly_garchomp_set):
    assert not hasattr(jolly_garchomp_set, "learnset")
    assert {field.name for field in fields(jolly_garchomp_set)} == {
        "species",
        "level",
        "nature",
        "ivs",
        "evs",
        "moves",
        "ability",
    }


def test_pokemon_set_is_immutable(jolly_garchomp_set):
    with pytest.raises(FrozenInstanceError):
        jolly_garchomp_set.level = 100


def test_pokemon_from_set_calculates_stats(jolly_garchomp_set):
    pokemon = Pokemon.from_set(jolly_garchomp_set)

    assert pokemon.stats.speed == 169
    assert pokemon.stats.attack == 182


def test_negative_hp_is_fainted(jolly_garchomp_set):
    pokemon = Pokemon.from_set(jolly_garchomp_set)

    pokemon.current_hp = -10

    assert pokemon.is_fainted


def test_from_components_accepts_valid_learnset_moves(
    jolly_garchomp_set,
    tackle,
    earthquake,
    dragon_claw,
    swords_dance,
):
    configured_set = PokemonSet.from_components(
        species=jolly_garchomp_set.species,
        level=jolly_garchomp_set.level,
        nature=jolly_garchomp_set.nature,
        ivs=jolly_garchomp_set.ivs,
        evs=jolly_garchomp_set.evs,
        moves=(tackle, earthquake, dragon_claw, swords_dance),
        ability=jolly_garchomp_set.ability,
        learnset=frozenset(
            {
                "TACKLE",
                "EARTHQUAKE",
                "DRAGON_CLAW",
                "SWORDS_DANCE",
            }
        ),
    )

    assert configured_set.moves == (
        tackle,
        earthquake,
        dragon_claw,
        swords_dance,
    )
