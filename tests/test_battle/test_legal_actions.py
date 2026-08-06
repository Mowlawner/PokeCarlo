from battle.action import MoveAction
from battle.decision.legal_actions import get_legal_actions


def test_get_legal_actions_returns_moves(
    battle_context,
    garchomp,
):
    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    assert len(actions) == len(garchomp.pokemon_set.moves)
    assert all(isinstance(action, MoveAction) for action in actions)


def test_move_actions_reference_actor(
    battle_context,
    garchomp,
):
    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    for action in actions:
        assert action.actor is garchomp
