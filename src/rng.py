import random


class RNG:
    def __init__(self, seed: int) -> None:
        self.random = random.Random(seed)

    def roll(self):
        return self.random.random()
