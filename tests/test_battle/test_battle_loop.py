# tests/test_battle/test_battle_loop.py

from battle.action import MoveAction
from battle_loop import execute_turn


class RecordingAI:
    def __init__(self, action):
        self.action = action
        self.received_legal_actions = None
        self.received_pokemon = None

    def choose_action(
        self,
        *,
        battle_context,
        pokemon,
        legal_actions,
    ):
        self.received_legal_actions = legal_actions
        self.received_pokemon = pokemon
        return self.action


def test_execute_turn_requests_actions_from_both_ais(
    battle_context,
    garchomp,
    opponent_garchomp,
):
    player_action = MoveAction(
        actor=garchomp,
        move=garchomp.pokemon_set.moves[0],
        target=opponent_garchomp,
    )

    opponent_action = MoveAction(
        actor=opponent_garchomp,
        move=opponent_garchomp.pokemon_set.moves[0],
        target=garchomp,
    )

    player_ai = RecordingAI(player_action)
    opponent_ai = RecordingAI(opponent_action)

    execute_turn(
        player_ai=player_ai,
        opponent_ai=opponent_ai,
        battle_context=battle_context,
    )

    assert player_ai.received_pokemon is garchomp
    assert opponent_ai.received_pokemon is opponent_garchomp

    assert player_ai.received_legal_actions
    assert opponent_ai.received_legal_actions


def test_execute_turn_selected_actions_are_from_legal_action_sets(
    battle_context,
    garchomp,
    opponent_garchomp,
):
    player_action = MoveAction(
        actor=garchomp,
        move=garchomp.pokemon_set.moves[0],
        target=opponent_garchomp,
    )

    opponent_action = MoveAction(
        actor=opponent_garchomp,
        move=opponent_garchomp.pokemon_set.moves[0],
        target=garchomp,
    )

    player_ai = RecordingAI(player_action)
    opponent_ai = RecordingAI(opponent_action)

    execute_turn(
        player_ai=player_ai,
        opponent_ai=opponent_ai,
        battle_context=battle_context,
    )

    assert player_ai.action in player_ai.received_legal_actions
    assert opponent_ai.action in opponent_ai.received_legal_actions
