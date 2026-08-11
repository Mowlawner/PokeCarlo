from collections import deque


class StubRNG:
    def __init__(
        self,
        *,
        accuracy_rolls: list[float] | None = None,
        damage_rolls: list[float] | None = None,
        critical_rolls: list[float] | None = None,
        rolls: list[float] | None = None,
        choices: list[int] | None = None,
    ):
        self._accuracy_rolls = accuracy_rolls or [0.0]
        self._damage_rolls = damage_rolls or [1.0]
        self._critical_rolls = critical_rolls or [1.0]
        self._rolls = rolls or [0.0]
        self._choices = deque(choices or [])

    def accuracy_roll(self) -> float:
        return self._accuracy_rolls.pop(0)

    def damage_roll(self) -> float:
        return self._damage_rolls.pop(0)

    def critical_roll(self) -> float:
        return self._critical_rolls.pop(0)

    def roll(self) -> float:
        return self._rolls.pop(0)

    def choice[T](self, values: tuple[T, ...]) -> T:
        if not values:
            raise ValueError("Cannot choose from an empty sequence.")

        index = self._choices.popleft()

        return values[index]
