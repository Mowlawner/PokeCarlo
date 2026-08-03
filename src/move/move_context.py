from dataclasses import dataclass

from pokemon_types import Type


@dataclass(frozen=True, slots=True)
class MoveContext:
    move_type: Type
