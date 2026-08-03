from battle.rng import RNG
from battle_ai.ai import AI


class RandomAI(AI):
    def choose_move(self, pokemon, rng: RNG):
        return rng.random.choice(pokemon.moves)
