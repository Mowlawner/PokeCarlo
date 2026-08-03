from dataclasses import dataclass
from pokemon_types import Type

@dataclass(slots=True, frozen=True)
class Move:
    name: str

    power: int

    accuracy: int

    move_type: Type

    category: str

    priority: int = 0
