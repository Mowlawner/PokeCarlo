from battle import Action
from battle.action import MoveAction
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

    return tuple(actions)
