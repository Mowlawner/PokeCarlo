from dataclasses import FrozenInstanceError

import pytest

from abilities.ability import Ability
from abilities.low_hp_type_boost_ability import (
    BLAZE,
    TORRENT,
)
from battle import BattleState
from battle.battle_context import BattleContext
from battle.stub_rng import StubRNG
from pokemon_types import Type
from stats.stat import Stat
from stats.stat_engine import StatRole


def test_ability_can_be_created():
    ability = BLAZE

    assert ability.name == "Blaze"


def test_ability_is_immutable():
    ability = BLAZE

    with pytest.raises(FrozenInstanceError):
        ability.boost_type = Type.WATER


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
    garchomp, battle_context, move_context_factory
):
    ability = BLAZE

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
    ability = BLAZE

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
    ability = BLAZE

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
    ability = Ability()

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


def test_intimidate_lowers_opponents_attack_by_one_stage(garchomp, gyarados):
    gyarados.pokemon_set.ability.on_switch_in(
        pokemon=gyarados,
        battle_context=BattleContext(
            state=BattleState(
                player_active=(gyarados,),
                opponent_active=(garchomp,),
                turn_number=1,
            ),
            rng=StubRNG(),
        ),
    )
    assert garchomp.stat_stages.attack == -1
