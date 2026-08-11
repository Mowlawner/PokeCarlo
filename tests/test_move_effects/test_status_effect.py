from battle import BattleContext, StubRNG
from move_effects.move_effect import (
    DamageDealt,
    MoveEffectResult,
    StatusApplicationOutcome,
)
from move_effects.status_effect import StatusEffect
from status_condition import StatusCondition


def damage_result(target, amount=1):
    return MoveEffectResult(
        applied=amount > 0,
        damage_dealt=(DamageDealt(target=target, amount=amount),),
    )


def test_status_effect_applies_paralysis_to_healthy_target(
    garchomp,
    opponent_garchomp,
    battle_context,
    move_context_factory,
):
    result = StatusEffect(StatusCondition.PARALYSIS).apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context_factory(garchomp.pokemon_set.moves[0].move_type),
        battle_context=battle_context,
    )

    assert opponent_garchomp.status is StatusCondition.PARALYSIS
    assert result.applied
    assert result.status_applications[0].outcome is StatusApplicationOutcome.APPLIED


def test_status_effect_reports_existing_status_without_overwriting(
    garchomp,
    opponent_garchomp,
    battle_context,
    move_context_factory,
):
    opponent_garchomp.status = StatusCondition.BURN

    result = StatusEffect(StatusCondition.PARALYSIS).apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context_factory(garchomp.pokemon_set.moves[0].move_type),
        battle_context=battle_context,
    )

    assert opponent_garchomp.status is StatusCondition.BURN
    assert not result.applied
    assert (
        result.status_applications[0].outcome
        is StatusApplicationOutcome.ALREADY_AFFECTED_BY_OTHER_STATUS
    )


def test_status_effect_reports_reapplying_same_status(
    garchomp,
    opponent_garchomp,
    battle_context,
    move_context_factory,
):
    opponent_garchomp.status = StatusCondition.PARALYSIS

    result = StatusEffect(StatusCondition.PARALYSIS).apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context_factory(garchomp.pokemon_set.moves[0].move_type),
        battle_context=battle_context,
    )

    assert opponent_garchomp.status is StatusCondition.PARALYSIS
    assert not result.applied
    assert (
        result.status_applications[0].outcome
        is StatusApplicationOutcome.ALREADY_AFFECTED
    )


def test_chance_status_applies_after_damage(
    battle_context, garchomp, opponent_garchomp, move_context_factory
):
    result = StatusEffect(StatusCondition.BURN, chance=10).apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context_factory(garchomp.pokemon_set.moves[0].move_type),
        battle_context=BattleContext(battle_context.state, StubRNG(rolls=[0.09])),
        prior_results=(damage_result(opponent_garchomp),),
    )

    assert opponent_garchomp.status is StatusCondition.BURN
    assert result.applied


def test_chance_status_skips_failed_roll_and_zero_damage_is_still_a_hit(
    battle_context, garchomp, opponent_garchomp, move_context_factory
):
    result = StatusEffect(StatusCondition.BURN, chance=10).apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context_factory(garchomp.pokemon_set.moves[0].move_type),
        battle_context=BattleContext(battle_context.state, StubRNG(rolls=[0.10])),
        prior_results=(damage_result(opponent_garchomp, amount=0),),
    )

    assert opponent_garchomp.status is StatusCondition.NONE
    assert result.status_applications == ()


def test_lethal_damage_skips_secondary_status(
    battle_context, garchomp, opponent_garchomp, move_context_factory
):
    opponent_garchomp.current_hp = 0
    rng = StubRNG(rolls=[0.0])

    result = StatusEffect(StatusCondition.BURN, chance=100).apply(
        user=garchomp,
        targets=(opponent_garchomp,),
        move_context=move_context_factory(garchomp.pokemon_set.moves[0].move_type),
        battle_context=BattleContext(battle_context.state, rng),
        prior_results=(damage_result(opponent_garchomp, amount=100),),
    )

    assert result.status_applications == ()
    assert rng._rolls == [0.0]


def test_chance_status_rolls_independently_for_each_target(
    battle_context, garchomp, opponent_garchomp, move_context_factory
):
    result = StatusEffect(StatusCondition.BURN, chance=50).apply(
        user=garchomp,
        targets=(opponent_garchomp, garchomp),
        move_context=move_context_factory(garchomp.pokemon_set.moves[0].move_type),
        battle_context=BattleContext(battle_context.state, StubRNG(rolls=[0.0, 0.5])),
        prior_results=(
            MoveEffectResult(
                applied=True,
                damage_dealt=(
                    DamageDealt(opponent_garchomp, 1),
                    DamageDealt(garchomp, 1),
                ),
            ),
        ),
    )

    assert result.applied
    assert len(result.status_applications) == 1
