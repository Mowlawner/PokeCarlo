from typing import Protocol

from battle.action import Action
from battle.battle_context import BattleContext
from pokemon import Pokemon


class BattleAI(Protocol):
    def choose_action(
        self,
        *,
        battle_context: BattleContext,
        pokemon: Pokemon,
        legal_actions: tuple[Action, ...],
    ) -> Action: ...
