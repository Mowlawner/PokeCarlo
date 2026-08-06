from abc import ABC
from dataclasses import dataclass

from battle.battle_context import BattleContext
from move import Move
from pokemon import Pokemon


class Action(ABC):
    actor: Pokemon

    @property
    def priority(self) -> int:
        return 0

    def speed_tiebreaker(self) -> int:
        return self.actor.stats.speed

    def apply(self, context: BattleContext) -> None:
        if self.actor.is_fainted:
            return

        self._apply(context)

    def _apply(self, context: BattleContext) -> None:
        pass


@dataclass(slots=True)
class MoveAction(Action):
    actor: Pokemon
    move: Move
    target: Pokemon | None = None

    @property
    def priority(self) -> int:
        return self.move.priority

    def _apply(self, context: BattleContext) -> None:
        targets = context.get_targets(
            user=self.actor,
            targeting=self.move.targeting,
        )

        self.move.apply(
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

        self.incoming.pokemon_set.ability.on_switch_in(
            pokemon=self.incoming,
            battle_context=context,
        )


### OLD ###
# from dataclasses import dataclass
# from enum import Enum, auto
#
# from battle.battle_context import BattleContext
# from move import Move
# from pokemon import Pokemon
#
#
# class ActionType(Enum):
#     MOVE = auto()
#     SWITCH = auto()
#
#
# class Action:
#     actor: Pokemon
#
# @dataclass(slots=True)
# class MoveAction(Action):
#     actor: Pokemon
#     move: Move
#
# @dataclass(slots=True)
# class SwitchAction(Action):
#     actor: Pokemon
#     incoming: Pokemon
#
#     def apply(
#         self,
#         context: BattleContext,
#     ) -> None:
#         if self.actor.is_fainted:
#             return
#         match self.action:
#             case ActionType.MOVE:
#                 if self.move is not None:
#                     move_targets = context.get_targets(
#                         self.pokemon, self.move.targeting, self.target
#                     )
#                     self.move.apply(
#                         user=self.pokemon, targets=move_targets, battle_context=context
#                     )
#                 else:
#                     raise ValueError("A move action must have a move, none was given.")
#             case ActionType.SWITCH:
#                 if self.target is not None:
#                     if self.move is not None:
#                         raise ValueError(
#                             f"A switch action may not specify a move, {self.move} was given."
#                         )
#                     raise NotImplementedError
#                 else:
#                     raise ValueError(
#                         "A switch action must have a target, none was given."
#                     )
