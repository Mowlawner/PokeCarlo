from dataclasses import dataclass
from typing import TYPE_CHECKING

from battle.battle_context import BattleContext
from move.move_context import MoveContext
from move_effects.move_effect import MoveEffectResult, StatStageChange
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
        move_context: MoveContext,
        battle_context: BattleContext,
    ) -> MoveEffectResult:
        changes = []
        for target in targets:
            actual_change = modify_stage(
                target.stat_stages,
                self.stat,
                self.stages,
            )
            if actual_change:
                changes.append(
                    StatStageChange(
                        target=target,
                        stat=self.stat,
                        amount=actual_change,
                    )
                )

        return MoveEffectResult(
            applied=bool(changes),
            stat_stage_changes=tuple(changes),
        )
