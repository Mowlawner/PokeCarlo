from dataclasses import dataclass

from src.move import Move
from src.pokemon_species import PokemonSpecies


@dataclass(slots=True)
class Pokemon:
    species: PokemonSpecies
    level: int
    current_hp: int
    moves: list[Move]

    @classmethod
    def from_species(
        cls,
        species: PokemonSpecies,
        level: int,
        moves: list[Move],
    ):
        return cls(
            species=species,
            level=level,
            current_hp=species.base_stats.hp,
            moves=moves,
        )
