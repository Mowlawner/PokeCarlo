from dataclasses import dataclass
from enum import Enum, auto

from battle.battle_context import BattleContext
from move import Move
from pokemon import Pokemon


class ActionType(Enum):
    MOVE = auto()
    SWITCH = auto()


@dataclass(frozen=True, slots=True)
class Action:
    pokemon: Pokemon
    action: ActionType
    move: Move | None = None
    target: Pokemon | None = None

    def apply(
        self,
        context: BattleContext,
    ) -> None:
        match self.action:
            case ActionType.MOVE:
                if self.move is not None:
                    move_targets = context.get_targets(
                        self.pokemon, self.move.targeting, self.target
                    )
                    self.move.apply(user=self.pokemon, targets=move_targets)
                else:
                    raise ValueError("A move action must have a move, none was given.")
            case ActionType.SWITCH:
                if self.target is not None:
                    if self.move is not None:
                        raise ValueError(
                            f"A switch action may not specify a move, {self.move} was given."
                        )
                    raise NotImplementedError
                else:
                    raise ValueError(
                        "A switch action must have a target, none was given."
                    )
