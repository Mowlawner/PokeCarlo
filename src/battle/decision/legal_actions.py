from battle import Action
from battle.action import MoveAction, SwitchAction
from battle.battle_context import BattleContext
from pokemon import Pokemon


def get_legal_actions(
    *,
    battle_context: BattleContext,
    pokemon: Pokemon,
) -> tuple[Action, ...]:
    actions = []

    # TODO: implement PP system
    for move in pokemon.pokemon_set.moves:
        actions.append(
            MoveAction(
                actor=pokemon,
                move=move,
            )
        )

    for bench_pokemon in battle_context.get_bench(pokemon):
        actions.append(
            SwitchAction(
                actor=pokemon,
                incoming=bench_pokemon,
            )
        )

    return tuple(actions)
