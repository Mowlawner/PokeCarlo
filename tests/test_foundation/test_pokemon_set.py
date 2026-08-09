from dataclasses import FrozenInstanceError, fields, replace

import pytest

from abilities.intimidate import Intimidate
from abilities.low_hp_type_boost_ability import Blaze
from abilities.not_implemented_abilities import RoughSkin
from ability import Ability
from item import Item
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
    assert isinstance(pokemon.ability, RoughSkin)

    assert pokemon.current_hp == pokemon.stats.hp
    assert pokemon.stat_stages == StatStages()

    pokemon.current_hp = 0

    assert pokemon.is_fainted

    pokemon.current_hp = 1

    assert not pokemon.is_fainted


def test_from_set_resolves_intimidate(jolly_gyarados_set):
    pokemon = Pokemon.from_set(jolly_gyarados_set)

    assert isinstance(pokemon.ability, Intimidate)
    assert pokemon.pokemon_set.ability.name == "INTIMIDATE"


def test_from_set_resolves_blaze(jolly_garchomp_set):
    blaze = Ability(
        name="BLAZE",
        display_name="Blaze",
        id=66,
        generation="GENERATION_III",
    )
    blaze_species = replace(jolly_garchomp_set.species, abilities=("BLAZE",))
    blaze_set = replace(
        jolly_garchomp_set,
        species=blaze_species,
        ability=blaze,
    )

    pokemon = Pokemon.from_set(blaze_set)

    assert isinstance(pokemon.ability, Blaze)
    assert pokemon.pokemon_set.ability is blaze


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
        "item",
    }


def test_pokemon_set_is_immutable(jolly_garchomp_set):
    with pytest.raises(FrozenInstanceError):
        jolly_garchomp_set.level = 100


def test_pokemon_from_set_calculates_stats(jolly_garchomp_set):
    pokemon = Pokemon.from_set(jolly_garchomp_set)

    assert pokemon.stats.speed == 169
    assert pokemon.stats.attack == 182


def test_pokemon_set_defaults_to_no_item(jolly_garchomp_set):
    assert jolly_garchomp_set.item is None


def test_pokemon_set_can_store_an_item(jolly_garchomp_set):
    item = Item(
        name="LEFTOVERS",
        display_name="Leftovers",
        id=211,
        category="HELD_ITEMS",
        attributes=("HOLDABLE", "HOLDABLE_ACTIVE"),
    )

    configured_set = replace(jolly_garchomp_set, item=item)

    assert configured_set.item is item


def test_pokemon_from_set_preserves_item(jolly_garchomp_set):
    item = Item(
        name="LEFTOVERS",
        display_name="Leftovers",
        id=211,
        category="HELD_ITEMS",
        attributes=("HOLDABLE", "HOLDABLE_ACTIVE"),
    )
    configured_set = replace(jolly_garchomp_set, item=item)

    pokemon_with_item = Pokemon.from_set(configured_set)
    pokemon_without_item = Pokemon.from_set(jolly_garchomp_set)

    assert pokemon_with_item.pokemon_set.item is item
    assert pokemon_without_item.pokemon_set.item is None


def test_pokemon_set_item_is_immutable(jolly_garchomp_set):
    item = Item("LEFTOVERS", "Leftovers", 211, "HELD_ITEMS", ())
    configured_set = replace(jolly_garchomp_set, item=item)

    with pytest.raises(FrozenInstanceError):
        configured_set.item = None


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
