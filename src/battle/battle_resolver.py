from battle.action import Action
from battle.battle_context import BattleContext


class BattleResolver:
    def __init__(self, context: BattleContext):
        self.context = context

    def resolve_turn(
        self,
        actions: tuple[Action, ...],
    ) -> None:
        for action in actions:
            action.apply(self.context)
