from move import MoveCategory
from move_effects.damage_effect import DamageEffect, resolve_defaults
from stats.stat import Stat


def test_physical_defaults():
    effect = resolve_defaults(
        DamageEffect(),
        MoveCategory.PHYSICAL,
    )

    assert effect.attacking_stat is Stat.ATTACK
    assert effect.defending_stat is Stat.DEFENSE


def test_special_defaults():
    effect = resolve_defaults(
        DamageEffect(),
        MoveCategory.SPECIAL,
    )

    assert effect.attacking_stat is Stat.SP_ATTACK
    assert effect.defending_stat is Stat.SP_DEFENSE


def test_attack_stat_override():
    effect = resolve_defaults(
        DamageEffect(
            attacking_stat=Stat.DEFENSE,
        ),
        MoveCategory.PHYSICAL,
    )

    assert effect.attacking_stat is Stat.DEFENSE
    assert effect.defending_stat is Stat.DEFENSE


def test_defending_stat_override():
    effect = resolve_defaults(
        DamageEffect(
            defending_stat=Stat.SP_DEFENSE,
        ),
        MoveCategory.PHYSICAL,
    )

    assert effect.attacking_stat is Stat.ATTACK
    assert effect.defending_stat is Stat.SP_DEFENSE


def test_both_stats_can_be_overridden():
    effect = resolve_defaults(
        DamageEffect(
            attacking_stat=Stat.DEFENSE,
            defending_stat=Stat.ATTACK,
        ),
        MoveCategory.PHYSICAL,
    )

    assert effect.attacking_stat is Stat.DEFENSE
    assert effect.defending_stat is Stat.ATTACK
