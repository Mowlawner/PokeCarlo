from abilities.ability import Ability
from battle.battle_context import BattleContext
from battle.stub_rng import StubRNG
from move import MoveCategory
from move.move_context import MoveContext
from move_effects.damage_effect import DamageEffect, resolve_defaults
from stats.stat import Stat
from stats.stat_utils import modify_stage
from status_condition import StatusCondition


def test_physical_defaults():
    effect = resolve_defaults(
        DamageEffect(power=100),
        MoveCategory.PHYSICAL,
    )

    assert effect.attacking_stat is Stat.ATTACK
    assert effect.defending_stat is Stat.DEFENSE


def test_special_defaults():
    effect = resolve_defaults(
        DamageEffect(power=100),
        MoveCategory.SPECIAL,
    )

    assert effect.attacking_stat is Stat.SP_ATTACK
    assert effect.defending_stat is Stat.SP_DEFENSE


def test_attack_stat_override():
    effect = resolve_defaults(
        DamageEffect(
            attacking_stat=Stat.DEFENSE,
            power=100,
        ),
        MoveCategory.PHYSICAL,
    )

    assert effect.attacking_stat is Stat.DEFENSE
    assert effect.defending_stat is Stat.DEFENSE


def test_defending_stat_override():
    effect = resolve_defaults(
        DamageEffect(
            defending_stat=Stat.SP_DEFENSE,
            power=100,
        ),
        MoveCategory.PHYSICAL,
    )

    assert effect.attacking_stat is Stat.ATTACK
    assert effect.defending_stat is Stat.SP_DEFENSE


def test_both_stats_can_be_overridden():
    effect = resolve_defaults(
        DamageEffect(
            attacking_stat=Stat.DEFENSE, defending_stat=Stat.ATTACK, power=100
        ),
        MoveCategory.PHYSICAL,
    )

    assert effect.attacking_stat is Stat.DEFENSE
    assert effect.defending_stat is Stat.ATTACK


def test_damage_effect_reduces_hp(
    garchomp,
    earthquake,
    battle_context,
):
    effects = earthquake.effects

    starting_hp = garchomp.current_hp

    for effect in effects:
        effect.apply(
            user=garchomp,
            targets=(garchomp,),
            move_context=MoveContext(earthquake.move_type, earthquake.category),
            battle_context=battle_context,
        )

    assert garchomp.current_hp < starting_hp


def test_damage_effect_uses_attack_stat_stage(
    garchomp,
    opponent_garchomp,
    tackle,
    battle_state,
):
    move_context = MoveContext(tackle.move_type, tackle.category)

    opponent_garchomp.current_hp = opponent_garchomp.stats.hp
    tackle.effects[0].apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context,
        battle_context=BattleContext(
            battle_state,
            StubRNG(critical_rolls=[1.0], damage_rolls=[1.0]),
        ),
    )
    normal_damage = opponent_garchomp.stats.hp - opponent_garchomp.current_hp

    modify_stage(garchomp.stat_stages, Stat.ATTACK, 2)
    opponent_garchomp.current_hp = opponent_garchomp.stats.hp
    tackle.effects[0].apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context,
        battle_context=BattleContext(
            battle_state,
            StubRNG(critical_rolls=[1.0], damage_rolls=[1.0]),
        ),
    )
    boosted_damage = opponent_garchomp.stats.hp - opponent_garchomp.current_hp

    assert boosted_damage > normal_damage


def test_damage_effect_uses_burned_physical_attack(
    garchomp,
    opponent_garchomp,
    tackle,
    battle_state,
):
    move_context = MoveContext(tackle.move_type, tackle.category)
    opponent_garchomp.current_hp = opponent_garchomp.stats.hp
    tackle.effects[0].apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context,
        battle_context=BattleContext(
            battle_state,
            StubRNG(critical_rolls=[1.0], damage_rolls=[1.0]),
        ),
    )
    normal_damage = opponent_garchomp.stats.hp - opponent_garchomp.current_hp

    garchomp.status = StatusCondition.BURN
    opponent_garchomp.current_hp = opponent_garchomp.stats.hp
    tackle.effects[0].apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context,
        battle_context=BattleContext(
            battle_state,
            StubRNG(critical_rolls=[1.0], damage_rolls=[1.0]),
        ),
    )
    burned_damage = opponent_garchomp.stats.hp - opponent_garchomp.current_hp

    assert burned_damage < normal_damage


def test_damage_effect_uses_runtime_ability_stat_modifier(
    garchomp,
    opponent_garchomp,
    tackle,
    battle_state,
):
    class AttackBoost(Ability):
        name = "TEST_ATTACK_BOOST"

        def modify_effective_stat(
            self,
            *,
            value,
            pokemon,
            stat,
            role,
            move_context,
            battle_context,
        ):
            if stat is Stat.ATTACK:
                return value + 50
            return value

    move_context = MoveContext(tackle.move_type, tackle.category)
    opponent_garchomp.current_hp = opponent_garchomp.stats.hp
    tackle.effects[0].apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context,
        battle_context=BattleContext(
            battle_state,
            StubRNG(critical_rolls=[1.0], damage_rolls=[1.0]),
        ),
    )
    normal_damage = opponent_garchomp.stats.hp - opponent_garchomp.current_hp

    garchomp.ability = AttackBoost()
    opponent_garchomp.current_hp = opponent_garchomp.stats.hp
    tackle.effects[0].apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context,
        battle_context=BattleContext(
            battle_state,
            StubRNG(critical_rolls=[1.0], damage_rolls=[1.0]),
        ),
    )
    boosted_damage = opponent_garchomp.stats.hp - opponent_garchomp.current_hp

    assert boosted_damage > normal_damage
