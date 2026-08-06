from battle import BattleContext, BattleState, StubRNG
from battle.action import MoveAction
from battle.decision.legal_actions import get_legal_actions
from battle_ai.random_ai import RandomAI


def test_random_ai_selects_legal_action(
    battle_context,
    garchomp,
):
    actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=garchomp,
    )

    ai = RandomAI()

    selected = ai.choose_action(
        battle_context=battle_context,
        pokemon=garchomp,
        legal_actions=actions,
    )

    assert selected in actions


def test_random_ai_uses_rng_choice(
    garchomp,
):
    actions = (
        MoveAction(actor=garchomp, move=garchomp.pokemon_set.moves[0]),
        MoveAction(actor=garchomp, move=garchomp.pokemon_set.moves[0]),
    )

    battle_context = BattleContext(
        state=BattleState(
            player_active=(garchomp,),
            opponent_active=(),
        ),
        rng=StubRNG(choices=[1]),
    )

    ai = RandomAI()

    selected = ai.choose_action(
        battle_context=battle_context,
        pokemon=garchomp,
        legal_actions=actions,
    )

    assert selected is actions[1]
