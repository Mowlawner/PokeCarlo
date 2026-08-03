from src.battle_ai.ai import AI
from src.rng import RNG


class RandomAI(AI):
    def choose_move(self, pokemon, rng: RNG):
        return rng.random.choice(pokemon.moves)
