from dataclasses import dataclass

from abilities.ability import Ability
from pokemon_types import Type
from stats.base_stats import BaseStats


@dataclass(slots=True, frozen=True)
class PokemonSpecies:
    name: str

    types: tuple[Type, ...]

    base_stats: BaseStats

    abilities: tuple[Ability, ...]

    def __post_init__(self):
        if len(set(self.types)) != len(self.types):
            raise ValueError("Pokemon cannot have duplicate types.")

        if len(self.types) not in (1, 2):
            raise ValueError("Pokemon must have one or two types.")

        if len(self.abilities) == 0:
            raise ValueError("Species must have at least one ability.")

        if len(set(self.abilities)) != len(self.abilities):
            raise ValueError("Species cannot have duplicate abilities.")

    @classmethod
    def from_json(cls, json_data: dict, name: str):
        raise NotImplementedError(
            "PokemonSpecies.from_json() has not been updated to load abilities yet."
        )
        return PokemonSpecies(
            name=name,
            types=tuple(Type(t) for t in json_data["pokemon_types"]),
            base_stats=BaseStats.from_json(json_data["base_stats"]),
            abilities=(),
        )
