from move import MoveTarget


def test_self_target_returns_user(garchomp, battle_context):
    targets = battle_context.resolve_targets(
        user=garchomp,
        targeting=MoveTarget.SELF,
    )

    assert targets == (garchomp,)


def test_single_target_returns_selected_target(
    garchomp,
    opponent_garchomp,
    battle_context,
):
    targets = battle_context.resolve_targets(
        user=garchomp,
        targeting=MoveTarget.SINGLE_TARGET,
        selected_target=opponent_garchomp,
    )

    assert targets == (opponent_garchomp,)


def test_all_opponents_returns_all_opponents(
    garchomp,
    opponent_garchomp,
    second_opponent_garchomp,
    battle_context,
):
    targets = battle_context.resolve_targets(
        user=garchomp,
        targeting=MoveTarget.ALL_OPPONENTS,
    )

    assert targets == (
        opponent_garchomp,
        second_opponent_garchomp,
    )


def test_all_others_excludes_user(
    garchomp,
    ally_garchomp,
    opponent_garchomp,
    second_opponent_garchomp,
    battle_context,
):
    targets = battle_context.resolve_targets(
        user=garchomp,
        targeting=MoveTarget.ALL_OTHERS,
    )

    assert targets == (
        ally_garchomp,
        opponent_garchomp,
        second_opponent_garchomp,
    )


def test_all_includes_user(
    garchomp,
    ally_garchomp,
    opponent_garchomp,
    second_opponent_garchomp,
    battle_context,
):
    targets = battle_context.resolve_targets(
        user=garchomp,
        targeting=MoveTarget.ALL,
    )

    assert targets == (
        garchomp,
        ally_garchomp,
        opponent_garchomp,
        second_opponent_garchomp,
    )
