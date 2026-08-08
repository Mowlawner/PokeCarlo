from dataclasses import dataclass

from abilities.ability import Ability
from move import Move
from pokemon_species import Species
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature


@dataclass(slots=True, frozen=True)
class PokemonSet:
    species: Species

    level: int

    nature: Nature

    ivs: IVs

    evs: EVs

    moves: tuple[Move, ...]

    ability: Ability

    def __post_init__(self) -> None:
        if not 1 <= len(self.moves) <= 4:
            raise ValueError("Pokemon must know between 1 and 4 moves.")
        if len(set(self.moves)) != len(self.moves):
            raise ValueError("Duplicate moves are not allowed.")
        ability_names = self.species.abilities
        if self.ability.name not in ability_names:
            allowed = ", ".join(ability_names)
            raise ValueError(
                f"{self.ability.name} is not a valid ability for {self.species.name}. "
                f"Expected one of: {allowed}."
            )
