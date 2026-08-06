from battle import Action
from battle.action import MoveAction, SwitchAction
from battle.battle_context import BattleContext
from pokemon import Pokemon


def get_legal_actions(
    *,
    battle_context: BattleContext,
    pokemon: Pokemon,
) -> tuple[Action, ...]:
    actions: list[Action] = []

    for move in pokemon.pokemon_set.moves:
        targets = battle_context.get_targets(
            user=pokemon,
            targeting=move.targeting,
        )

        # For now, allow generation of a move action even when targeting
        # cannot be resolved. This will likely change when fainted/forced
        # switch states are implemented.
        if move.targeting.name == "SINGLE_TARGET" and not targets:
            continue

        for target in targets:
            actions.append(
                MoveAction(
                    actor=pokemon,
                    move=move,
                    target=target,
                )
            )

    for bench_pokemon in battle_context.get_bench(pokemon):
        if not bench_pokemon.is_fainted:
            actions.append(
                SwitchAction(
                    actor=pokemon,
                    incoming=bench_pokemon,
                )
            )

    return tuple(actions)
