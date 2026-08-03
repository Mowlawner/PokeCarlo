from dataclasses import dataclass

from pokemon_types import Type
from stats.base_stats import BaseStats


@dataclass(slots=True, frozen=True)
class PokemonSpecies:
    name: str

    types: tuple[Type, ...]

    base_stats: BaseStats

    def __post_init__(self):
        if len(set(self.types)) != len(self.types):
            raise ValueError("Pokemon cannot have duplicate types.")

        if len(self.types) not in (1, 2):
            raise ValueError("Pokemon must have one or two types.")

    @classmethod
    def from_json(cls, json_data: dict, name: str):
        return PokemonSpecies(
            name=name,
            types=tuple(Type(t) for t in json_data["pokemon_types"]),
            base_stats=BaseStats.from_json(json_data["base_stats"]),
        )
