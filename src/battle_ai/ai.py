from src.action import Action
from src.battle_state import BattleState


class AI:
    def choose_action(self, state: BattleState) -> Action:
        raise NotImplementedError
