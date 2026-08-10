from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Protocol

from move.move_context import MoveContext
from stats.stat import Stat
from status_condition import StatusCondition

if TYPE_CHECKING:
    from battle.battle_context import BattleContext
    from pokemon import Pokemon


@dataclass(frozen=True, slots=True)
class StatStageChange:
    target: "Pokemon"
    stat: Stat
    amount: int


@dataclass(frozen=True, slots=True)
class DamageDealt:
    target: "Pokemon"
    amount: int


@dataclass(frozen=True, slots=True)
class HPRecovered:
    target: "Pokemon"
    amount: int


class StatusApplicationOutcome(Enum):
    APPLIED = auto()
    ALREADY_AFFECTED = auto()
    ALREADY_AFFECTED_BY_OTHER_STATUS = auto()


@dataclass(frozen=True, slots=True)
class StatusApplication:
    target: "Pokemon"
    status: StatusCondition
    outcome: StatusApplicationOutcome


@dataclass(frozen=True, slots=True)
class MoveEffectResult:
    applied: bool
    stat_stage_changes: tuple[StatStageChange, ...] = ()
    damage_dealt: tuple[DamageDealt, ...] = ()
    hp_restored: tuple[HPRecovered, ...] = ()
    status_applications: tuple[StatusApplication, ...] = ()


class MoveEffect(Protocol):
    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
        move_context: MoveContext,
        battle_context: "BattleContext",
        prior_results: tuple[MoveEffectResult, ...] = (),
    ) -> MoveEffectResult: ...
