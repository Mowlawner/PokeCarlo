from dataclasses import FrozenInstanceError, replace

import pytest

from pokemon import Pokemon
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
