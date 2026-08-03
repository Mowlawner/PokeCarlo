from dataclasses import replace

import pytest

from pokemon import Pokemon
from stats.stat_stages import StatStages


def test_one_move_is_allowed(garchomp_set):
    replace(garchomp_set, moves=garchomp_set.moves)


def test_four_moves_are_allowed(
    garchomp_set,
    tackle,
    earthquake,
    dragon_claw,
    swords_dance,
):
    replace(
        garchomp_set,
        moves=(
            tackle,
            earthquake,
            dragon_claw,
            swords_dance,
        ),
    )


def test_zero_moves_raises(garchomp_set):
    with pytest.raises(ValueError):
        replace(
            garchomp_set,
            moves=(),
        )


def test_five_moves_raises(garchomp_set, tackle):
    with pytest.raises(ValueError):
        replace(
            garchomp_set,
            moves=(
                tackle,
                tackle,
                tackle,
                tackle,
                tackle,
            ),
        )


def test_from_set(garchomp_set):
    pokemon = Pokemon.from_set(garchomp_set)

    assert pokemon.pokemon_set is garchomp_set

    assert pokemon.current_hp == pokemon.stats.hp
    assert pokemon.stat_stages == StatStages()

    pokemon.current_hp = 0

    assert pokemon.is_fainted

    pokemon.current_hp = 1

    assert not pokemon.is_fainted


def test_duplicate_moves_raise(
    garchomp_set,
    tackle,
):
    with pytest.raises(ValueError):
        replace(
            garchomp_set,
            moves=(
                tackle,
                tackle,
            ),
        )
