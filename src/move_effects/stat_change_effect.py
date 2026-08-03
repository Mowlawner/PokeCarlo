from dataclasses import dataclass
from typing import TYPE_CHECKING

from stats.stat import Stat
from stats.stat_utils import modify_stage

if TYPE_CHECKING:
    from pokemon import Pokemon


@dataclass(frozen=True, slots=True)
class StatChangeEffect:
    stat: Stat
    stages: int

    def __post_init__(self):
        if self.stages == 0:
            raise ValueError("Stage changes cannot be zero.")

        if not -6 <= self.stages <= 6:
            raise ValueError(
                f"Stage change must be between -6 and 6, received: {self.stages}"
            )

    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
    ) -> None:
        for target in targets:
            modify_stage(
                target.stat_stages,
                self.stat,
                self.stages,
            )
