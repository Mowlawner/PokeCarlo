class StubRNG:
    def __init__(
        self,
        *,
        accuracy_rolls: list[float] | None = None,
        damage_rolls: list[float] | None = None,
        critical_rolls: list[float] | None = None,
    ):
        self._accuracy_rolls = accuracy_rolls or [0.0]
        self._damage_rolls = damage_rolls or [1.0]
        self._critical_rolls = critical_rolls or [1.0]

    def accuracy_roll(self) -> float:
        return self._accuracy_rolls.pop(0)

    def damage_roll(self) -> float:
        return self._damage_rolls.pop(0)

    def critical_roll(self) -> float:
        return self._critical_rolls.pop(0)
