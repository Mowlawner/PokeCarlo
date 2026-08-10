from dataclasses import dataclass
from typing import TYPE_CHECKING

from battle.battle_context import BattleContext
from move.move_context import MoveContext
from move_effects.move_effect import (
    MoveEffectResult,
    StatusApplication,
    StatusApplicationOutcome,
)
from status_condition import StatusCondition

if TYPE_CHECKING:
    from pokemon import Pokemon


@dataclass(frozen=True, slots=True)
class StatusEffect:
    status: StatusCondition

    def __post_init__(self) -> None:
        if self.status is StatusCondition.NONE:
            raise ValueError("StatusEffect requires a major status condition.")

    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
        move_context: MoveContext,
        battle_context: BattleContext,
        prior_results: tuple[MoveEffectResult, ...] = (),
    ) -> MoveEffectResult:
        applications = []

        for target in targets:
            if target.status is self.status:
                outcome = StatusApplicationOutcome.ALREADY_AFFECTED
            elif target.status is not StatusCondition.NONE:
                outcome = StatusApplicationOutcome.ALREADY_AFFECTED_BY_OTHER_STATUS
            else:
                target.status = self.status
                outcome = StatusApplicationOutcome.APPLIED

            applications.append(
                StatusApplication(
                    target=target,
                    status=self.status,
                    outcome=outcome,
                )
            )

        return MoveEffectResult(
            applied=any(
                application.outcome is StatusApplicationOutcome.APPLIED
                for application in applications
            ),
            status_applications=tuple(applications),
        )
