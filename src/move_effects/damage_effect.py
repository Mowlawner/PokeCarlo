from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pokemon import Pokemon


@dataclass(frozen=True, slots=True)
class DamageEffect:
    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
    ) -> None:
        pass
