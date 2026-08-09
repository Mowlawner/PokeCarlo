from abc import ABC
from dataclasses import dataclass

from battle.battle_context import BattleContext
from move import Move
from move.move import MoveExecutionResult
from pokemon import Pokemon


class Action(ABC):
    actor: Pokemon

    @property
    def priority(self) -> int:
        return 0

    def speed_tiebreaker(self) -> int:
        return self.actor.stats.speed

    def apply(self, context: BattleContext) -> MoveExecutionResult | None:
        if self.actor.is_fainted:
            return None

        return self._apply(context)

    def _apply(self, context: BattleContext) -> MoveExecutionResult | None:
        pass


@dataclass(slots=True)
class MoveAction(Action):
    actor: Pokemon
    move: Move
    target: Pokemon | None = None

    @property
    def priority(self) -> int:
        return self.move.priority

    def _apply(self, context: BattleContext) -> MoveExecutionResult:
        targets = context.resolve_targets(
            user=self.actor, targeting=self.move.targeting, selected_target=self.target
        )

        return self.move.apply(
            user=self.actor,
            targets=targets,
            battle_context=context,
        )


@dataclass(slots=True)
class SwitchAction(Action):
    actor: Pokemon
    incoming: Pokemon

    @property
    def priority(self) -> int:
        return 6

    def _apply(self, context: BattleContext) -> None:
        context.state.replace_active(
            outgoing=self.actor,
            incoming=self.incoming,
        )

        self.incoming.ability.on_switch_in(
            pokemon=self.incoming,
            battle_context=context,
        )
