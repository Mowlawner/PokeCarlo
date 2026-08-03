from dataclasses import dataclass

from stats.base_stats import BaseStats


@dataclass(slots=True, frozen=True)
class PokemonSpecies:
    name: str

    types: tuple[str, ...]

    base_stats: BaseStats

    @classmethod
    def from_json(cls, json_data: dict, name: str):
        return PokemonSpecies(
            name=name,
            types=tuple(json_data["types"]),
            base_stats=BaseStats.from_json(json_data["base_stats"]),
        )
