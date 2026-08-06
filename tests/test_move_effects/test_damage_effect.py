from move import MoveCategory
from move.move_context import MoveContext
from move_effects.damage_effect import DamageEffect, resolve_defaults
from stats.stat import Stat


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
