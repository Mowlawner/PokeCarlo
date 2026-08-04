from dataclasses import dataclass
from typing import TYPE_CHECKING

from pokemon_types import Type

if TYPE_CHECKING:
    from move import MoveCategory


@dataclass(frozen=True, slots=True)
class MoveContext:
    move_type: Type
    move_category: "MoveCategory"
