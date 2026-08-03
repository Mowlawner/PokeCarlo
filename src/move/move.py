from dataclasses import dataclass
from typing import TYPE_CHECKING

from move.move_category import MoveCategory
from move.targeting import MoveTarget
from move_effects.damage_effect import DamageEffect, resolve_defaults
from move_effects.move_effect import MoveEffect
from pokemon_types import Type

if TYPE_CHECKING:
    from pokemon import Pokemon


@dataclass(slots=True, frozen=True)
class Move:
    name: str
    accuracy: int | None
    move_type: Type
    category: MoveCategory
    effects: tuple[MoveEffect, ...]
    targeting: MoveTarget = MoveTarget.SINGLE_TARGET
    priority: int = 0

    def __post_init__(self):
        if self.accuracy is not None and not 1 <= self.accuracy <= 100:
            raise ValueError("Move accuracy must be between 1 and 100, or None.")

        if not -7 <= self.priority <= 5:
            raise ValueError("Invalid move priority.")

        object.__setattr__(
            self,
            "effects",
            tuple(
                resolve_defaults(effect, self.category)
                if isinstance(effect, DamageEffect)
                else effect
                for effect in self.effects
            ),
        )

        if self.category is MoveCategory.STATUS and any(
            isinstance(effect, DamageEffect) for effect in self.effects
        ):
            raise ValueError("Status moves cannot have DamageEffects.")

    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
    ) -> None:
        for effect in self.effects:
            effect.apply(user=user, targets=targets)
