from battle_ai.ai import AI
from rng import RNG


class RandomAI(AI):
    def choose_move(self, pokemon, rng: RNG):
        return rng.random.choice(pokemon.moves)
