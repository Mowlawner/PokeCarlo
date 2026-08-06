from battle.battle_context import BattleContext
from battle.battle_resolver import BattleResolver
from battle.decision.legal_actions import get_legal_actions
from battle.end_of_turn import apply_end_of_turn_effects
from battle_ai.ai import BattleAI


def battle(
    *,
    player_ai: BattleAI,
    opponent_ai: BattleAI,
    battle_context: BattleContext,
) -> None:
    resolver = BattleResolver(context=battle_context)

    while not battle_context.state.finished:
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

        apply_end_of_turn_effects(battle_context=battle_context)
