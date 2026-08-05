from dataclasses import FrozenInstanceError

import pytest

from abilities.ability import Ability
from abilities.low_hp_type_boost_ability import (
    BLAZE,
    TORRENT,
    LowHPTypeBoostAbility,
)
from pokemon_types import Type
from stats.stat import Stat
from stats.stat_engine import StatRole


def test_ability_can_be_created():
    ability = BLAZE

    assert ability.name == "Blaze"


def test_ability_is_immutable():
    ability = BLAZE

    with pytest.raises(FrozenInstanceError):
        ability.name = "Torrent"


def test_equal_abilities_compare_equal():
    ability1 = BLAZE
    ability2 = LowHPTypeBoostAbility(
        name="Blaze",
        boost_type=Type.FIRE,
    )

    assert ability1 == ability2


def test_different_abilities_compare_not_equal():
    assert BLAZE != TORRENT


def test_abilities_are_hashable():
    abilities = {
        BLAZE,
        TORRENT,
        BLAZE,
    }

    assert len(abilities) == 2


def test_low_hp_type_boost_ability_boosts_matching_type_damage(
    garchomp,
    battle_context,
    move_context_factory,
):
    ability = LowHPTypeBoostAbility(
        name="Test",
        boost_type=Type.FIRE,
    )

    garchomp.current_hp = garchomp.stats.hp // 3

    damage = ability.modify_outgoing_damage(
        damage=100,
        user=garchomp,
        target=garchomp,
        move_context=move_context_factory(move_type=Type.FIRE),
        battle_context=battle_context,
    )

    assert damage == 150


def test_low_hp_type_boost_ability_does_not_boost_wrong_type_damage(
    garchomp,
    battle_context,
    move_context_factory,
):
    ability = LowHPTypeBoostAbility(
        name="Test",
        boost_type=Type.FIRE,
    )

    garchomp.current_hp = garchomp.stats.hp // 3

    damage = ability.modify_outgoing_damage(
        damage=100,
        user=garchomp,
        target=garchomp,
        move_context=move_context_factory(move_type=Type.WATER),
        battle_context=battle_context,
    )

    assert damage == 100


def test_low_hp_type_boost_ability_does_not_boost_above_threshold(
    garchomp,
    battle_context,
    move_context_factory,
):
    ability = LowHPTypeBoostAbility(
        name="Test",
        boost_type=Type.FIRE,
    )

    garchomp.current_hp = garchomp.stats.hp

    damage = ability.modify_outgoing_damage(
        damage=100,
        user=garchomp,
        target=garchomp,
        move_context=move_context_factory(move_type=Type.FIRE),
        battle_context=battle_context,
    )

    assert damage == 100


def test_base_ability_does_not_modify_damage(
    garchomp,
    opponent_garchomp,
    battle_context,
    move_context_factory,
):
    ability = Ability(name="Test")

    assert (
        ability.modify_outgoing_damage(
            damage=100,
            user=garchomp,
            target=opponent_garchomp,
            move_context=move_context_factory(move_type=Type.FIRE),
            battle_context=battle_context,
        )
        == 100
    )
    assert (
        ability.modify_incoming_damage(
            damage=100,
            user=garchomp,
            target=opponent_garchomp,
            move_context=move_context_factory(move_type=Type.FIRE),
            battle_context=battle_context,
        )
        == 100
    )
    assert (
        ability.modify_effective_stat(
            value=100,
            pokemon=garchomp,
            stat=Stat.ATTACK,
            role=StatRole.DEFENSE,
            move_context=move_context_factory(move_type=Type.FIRE),
            battle_context=battle_context,
        )
        == 100
    )
