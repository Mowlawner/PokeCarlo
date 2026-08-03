from dataclasses import dataclass

from move import Move
from pokemon_species import PokemonSpecies
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature


@dataclass(slots=True, frozen=True)
class PokemonSet:
    species: PokemonSpecies

    level: int

    nature: Nature

    ivs: IVs

    evs: EVs

    moves: tuple[Move, ...]

    def __post_init__(self) -> None:
        if not 1 <= len(self.moves) <= 4:
            raise ValueError("Pokemon must know between 1 and 4 moves.")
        if len(set(self.moves)) != len(self.moves):
            raise ValueError("Duplicate moves are not allowed.")
