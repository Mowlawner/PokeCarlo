from battle.action import Action
from battle.battle_context import BattleContext
from pokemon import Pokemon


class RandomAI:
    def choose_action(
        self,
        *,
        battle_context: BattleContext,
        pokemon: Pokemon,
        legal_actions: tuple[Action, ...],
    ) -> Action:
        return battle_context.rng.choice(legal_actions)
