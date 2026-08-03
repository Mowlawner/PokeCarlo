from typing import TYPE_CHECKING, Protocol

from move.move_context import MoveContext

if TYPE_CHECKING:
    from pokemon import Pokemon


class MoveEffect(Protocol):
    def apply(
        self, user: "Pokemon", targets: tuple["Pokemon", ...], move_context: MoveContext
    ) -> None: ...
