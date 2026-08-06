import random


class RNG:
    """
    Single source of randomness for an entire simulated battle.

    All stochastic events—including AI decisions, move accuracy,
    critical hits, damage rolls, secondary effects, etc.—consume
    values from this stream to ensure deterministic replay from
    a single seed.
    """

    def __init__(self, seed: int) -> None:
        self._random = random.Random(seed)

    def roll(self) -> float:
        return self._random.random()

    def damage_roll(self) -> float:
        return self._random.uniform(0.85, 1.0)

    def accuracy_roll(self) -> float:
        return self.roll()

    def critical_roll(self) -> float:
        return self.roll()

    def choice[T](self, values: tuple[T, ...]) -> T:
        if not values:
            raise ValueError("Cannot choose from an empty sequence.")

        return values[self._random.randrange(len(values))]
