from dataclasses import dataclass
from enum import Enum, auto

from pokemon_types import Type


class MoveCategory(Enum):
    PHYSICAL = auto()
    SPECIAL = auto()
    STATUS = auto()


@dataclass(slots=True, frozen=True)
class Move:
    name: str

    power: int

    accuracy: int | None

    move_type: Type

    category: MoveCategory

    priority: int = 0

    def __post_init__(self):
        if self.power < 0:
            raise ValueError("Move power cannot be negative.")

        if self.accuracy is not None and not 1 <= self.accuracy <= 100:
            raise ValueError("Move accuracy must be between 1 and 100, or None.")

        if not -7 <= self.priority <= 5:
            raise ValueError("Invalid move priority.")
