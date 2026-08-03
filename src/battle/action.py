from dataclasses import dataclass
from enum import Enum, auto

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
