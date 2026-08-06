from battle.battle_context import BattleContext
from battle.battle_resolver import BattleResolver
from battle.decision.legal_actions import get_legal_actions
from battle.end_of_turn import apply_end_of_turn_effects
from battle_ai.ai import BattleAI


def execute_turn(
    *,
    player_ai: BattleAI,
    opponent_ai: BattleAI,
    battle_context: BattleContext,
) -> None:
    resolver = BattleResolver(context=battle_context)

    player_pokemon = battle_context.state.player_active[0]
    opponent_pokemon = battle_context.state.opponent_active[0]

    player_actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=player_pokemon,
    )

    opponent_actions = get_legal_actions(
        battle_context=battle_context,
        pokemon=opponent_pokemon,
    )

    player_action = player_ai.choose_action(
        battle_context=battle_context,
        pokemon=player_pokemon,
        legal_actions=player_actions,
    )

    opponent_action = opponent_ai.choose_action(
        battle_context=battle_context,
        pokemon=opponent_pokemon,
        legal_actions=opponent_actions,
    )

    resolver.resolve_turn(
        actions=(
            player_action,
            opponent_action,
        )
    )

    apply_end_of_turn_effects(
        battle_context=battle_context,
    )

    battle_context.state.turn_number += 1


def battle(
    *,
    player_ai: BattleAI,
    opponent_ai: BattleAI,
    battle_context: BattleContext,
    max_turns: int = 1,
) -> None:
    for _ in range(max_turns):
        execute_turn(
            player_ai=player_ai,
            opponent_ai=opponent_ai,
            battle_context=battle_context,
        )
