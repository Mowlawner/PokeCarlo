from move_effects.move_effect import StatusApplicationOutcome
from move_effects.status_effect import StatusEffect
from status_condition import StatusCondition


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
