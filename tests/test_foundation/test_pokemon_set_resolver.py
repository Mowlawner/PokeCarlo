import pytest

from ability import Ability
from database.ability_database import AbilityDatabase
from database.item_database import ItemDatabase
from database.learnset_database import LearnsetDatabase
from database.move_database import MoveDatabase
from database.species_database import SpeciesDatabase
from item import Item
from pokemon import Pokemon
from pokemon_set_resolver import PokemonSetResolver
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature


def make_resolver(garchomp_species, tackle, earthquake, protect):
    return PokemonSetResolver(
        species_database=SpeciesDatabase({garchomp_species.name: garchomp_species}),
        ability_database=AbilityDatabase(
            {
                "ROUGH_SKIN": Ability(
                    name="ROUGH_SKIN",
                    display_name="Rough Skin",
                    id=17,
                    generation="GENERATION_III",
                ),
                "INTIMIDATE": Ability(
                    name="INTIMIDATE",
                    display_name="Intimidate",
                    id=22,
                    generation="GENERATION_III",
                ),
            }
        ),
        move_database=MoveDatabase(
            {
                tackle.name: tackle,
                earthquake.name: earthquake,
                protect.name: protect,
            }
        ),
        item_database=ItemDatabase(
            {
                "LEFTOVERS": Item(
                    name="LEFTOVERS",
                    display_name="Leftovers",
                    id=211,
                    category="HELD_ITEMS",
                    attributes=("HOLDABLE", "HOLDABLE_ACTIVE"),
                )
            }
        ),
        learnset_database=LearnsetDatabase(
            {garchomp_species.name: frozenset({"TACKLE", "EARTHQUAKE"})}
        ),
    )


def resolve_defaults(resolver, moves=("TACKLE",), **kwargs):
    ability_name = kwargs.pop("ability_name", "rough-skin")
    return resolver.resolve(
        species_name="garchomp",
        ability_name=ability_name,
        move_names=moves,
        level=50,
        nature=Nature.JOLLY,
        ivs=IVs(31, 31, 31, 31, 31, 31),
        evs=EVs(6, 252, 0, 0, 0, 252),
        **kwargs,
    )


def test_resolver_builds_complete_set_and_preserves_move_order(
    garchomp_species,
    tackle,
    earthquake,
    protect,
):
    resolver = make_resolver(garchomp_species, tackle, earthquake, protect)

    pokemon_set = resolve_defaults(
        resolver,
        moves=("earthquake", "tackle"),
    )

    assert pokemon_set.species is garchomp_species
    assert pokemon_set.ability.name == "ROUGH_SKIN"
    assert pokemon_set.moves == (earthquake, tackle)
    assert pokemon_set.item is None


def test_resolver_resolves_optional_item(
    garchomp_species,
    tackle,
    earthquake,
    protect,
):
    resolver = make_resolver(garchomp_species, tackle, earthquake, protect)

    pokemon_set = resolve_defaults(resolver, item_name="leftovers")

    assert pokemon_set.item is not None
    assert pokemon_set.item.name == "LEFTOVERS"


def test_invalid_ability_is_rejected_by_pokemon_set(
    garchomp_species,
    tackle,
    earthquake,
    protect,
):
    resolver = make_resolver(garchomp_species, tackle, earthquake, protect)

    with pytest.raises(ValueError, match="not a valid ability"):
        resolve_defaults(resolver, ability_name="intimidate")


def test_unlearnable_move_is_rejected_by_pokemon_set(
    garchomp_species,
    tackle,
    earthquake,
    protect,
):
    resolver = make_resolver(garchomp_species, tackle, earthquake, protect)

    with pytest.raises(ValueError, match="cannot learn"):
        resolve_defaults(resolver, moves=("tackle", "protect"))


def test_resolved_set_constructs_pokemon(
    garchomp_species,
    tackle,
    earthquake,
    protect,
):
    resolver = make_resolver(garchomp_species, tackle, earthquake, protect)
    pokemon_set = resolve_defaults(resolver)

    pokemon = Pokemon.from_set(pokemon_set)

    assert pokemon.pokemon_set is pokemon_set
    assert pokemon.current_hp == pokemon.stats.hp
    assert not hasattr(pokemon_set, "learnset")
