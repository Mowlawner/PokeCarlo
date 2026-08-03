import random


class RNG:
    def __init__(self, seed: int) -> None:
        self._random = random.Random(seed)

    def roll(self):
        return self._random.random()

    def damage_roll(self) -> float:
        return self._random.uniform(0.85, 1.0)
