from typing import TYPE_CHECKING, Protocol

from move.move_context import MoveContext

if TYPE_CHECKING:
    from battle.battle_context import BattleContext
    from pokemon import Pokemon


class MoveEffect(Protocol):
    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
        move_context: MoveContext,
        battle_context: "BattleContext",
    ) -> None: ...
