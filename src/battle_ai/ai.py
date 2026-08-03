from action import Action
from battle_state import BattleState


class AI:
    def choose_action(self, state: BattleState) -> Action:
        raise NotImplementedError
