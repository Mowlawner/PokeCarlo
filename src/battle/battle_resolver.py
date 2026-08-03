from battle.action import Action
from battle.battle_context import BattleContext


class BattleResolver:
    def __init__(self, context: BattleContext):
        self.context = context

    def resolve_turn(
        self,
        actions: tuple[Action, ...],
    ) -> None:
        remaining_actions = list(actions)
        while remaining_actions:
            action = self.get_next_action(remaining_actions)
            remaining_actions.remove(action)

            action.apply(self.context)

    @staticmethod
    def get_next_action(
        actions: list[Action],
    ) -> Action:
        return max(
            actions,
            key=lambda action: (
                (action.move.priority, action.pokemon.stats.speed) if action.move else 0
            ),
        )
