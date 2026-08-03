from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pokemon import Pokemon


class MoveEffect(Protocol):
    def apply(
        self,
        user: "Pokemon",
        targets: tuple["Pokemon", ...],
    ) -> None: ...
