from move.move_context import MoveContext
from move_effects.healing_effect import HealingEffect
from move_effects.move_effect import DamageDealt, MoveEffectResult


def damage_result(*records):
    return MoveEffectResult(applied=True, damage_dealt=records)


def test_healing_consumes_actual_prior_damage(garchomp, tackle, battle_context):
    garchomp.current_hp = garchomp.stats.hp - 20
    effect = HealingEffect(healing_percent=50)

    result = effect.apply(
        user=garchomp,
        targets=(),
        move_context=MoveContext(tackle.move_type, tackle.category),
        battle_context=battle_context,
        prior_results=(damage_result(DamageDealt(target=garchomp, amount=11)),),
    )

    assert garchomp.current_hp == garchomp.stats.hp - 15
    assert result.applied
    assert result.hp_restored[0].target is garchomp
    assert result.hp_restored[0].amount == 5


def test_healing_uses_actual_damage_not_nominal_damage(
    garchomp, tackle, battle_context
):
    garchomp.current_hp = garchomp.stats.hp - 20
    result = HealingEffect(healing_percent=50).apply(
        user=garchomp,
        targets=(),
        move_context=MoveContext(tackle.move_type, tackle.category),
        battle_context=battle_context,
        prior_results=(damage_result(DamageDealt(target=garchomp, amount=3)),),
    )

    assert result.hp_restored[0].amount == 1
    assert garchomp.current_hp == garchomp.stats.hp - 19


def test_healing_is_capped_at_max_hp(garchomp, tackle, battle_context):
    garchomp.current_hp = garchomp.stats.hp - 1
    result = HealingEffect(healing_percent=100).apply(
        user=garchomp,
        targets=(),
        move_context=MoveContext(tackle.move_type, tackle.category),
        battle_context=battle_context,
        prior_results=(damage_result(DamageDealt(target=garchomp, amount=100)),),
    )

    assert result.applied
    assert result.hp_restored[0].amount == 1
    assert garchomp.current_hp == garchomp.stats.hp


def test_zero_damage_produces_zero_healing(garchomp, tackle, battle_context):
    result = HealingEffect().apply(
        user=garchomp,
        targets=(),
        move_context=MoveContext(tackle.move_type, tackle.category),
        battle_context=battle_context,
        prior_results=(damage_result(DamageDealt(target=garchomp, amount=0)),),
    )

    assert not result.applied
    assert result.hp_restored[0].amount == 0


def test_miss_produces_no_healing(garchomp, tackle, battle_context):
    result = HealingEffect().apply(
        user=garchomp,
        targets=(),
        move_context=MoveContext(tackle.move_type, tackle.category),
        battle_context=battle_context,
    )

    assert not result.applied
    assert result.hp_restored == ()


def test_multiple_targets_are_not_summed_without_explicit_request(
    garchomp, opponent_garchomp, second_opponent_garchomp, tackle, battle_context
):
    garchomp.current_hp = garchomp.stats.hp - 20
    prior_result = damage_result(
        DamageDealt(target=opponent_garchomp, amount=10),
        DamageDealt(target=second_opponent_garchomp, amount=20),
    )

    result = HealingEffect(healing_percent=100).apply(
        user=garchomp,
        targets=(),
        move_context=MoveContext(tackle.move_type, tackle.category),
        battle_context=battle_context,
        prior_results=(prior_result,),
    )

    assert result.hp_restored[0].amount == 10

    garchomp.current_hp = garchomp.stats.hp - 40
    aggregate_result = HealingEffect(
        healing_percent=100,
        aggregate_damage=True,
    ).apply(
        user=garchomp,
        targets=(),
        move_context=MoveContext(tackle.move_type, tackle.category),
        battle_context=battle_context,
        prior_results=(prior_result,),
    )

    assert aggregate_result.hp_restored[0].amount == 30


def test_healing_does_not_consume_future_effect_results(
    garchomp, tackle, battle_context
):
    garchomp.current_hp = garchomp.stats.hp - 20
    result = HealingEffect(healing_percent=100).apply(
        user=garchomp,
        targets=(),
        move_context=MoveContext(tackle.move_type, tackle.category),
        battle_context=battle_context,
        prior_results=(),
    )

    assert not result.applied
    assert garchomp.current_hp == garchomp.stats.hp - 20
