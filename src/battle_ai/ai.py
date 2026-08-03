from typing import Protocol

from battle.action import Action
from battle.battle_state import BattleState


class AI:
    class BattleAI(Protocol):
        def choose_action(
            self,
            state: BattleState,
        ) -> Action:
            raise NotImplementedError()
