from dataclasses import dataclass

from src.stats.stats import Stats


@dataclass(slots=True, frozen=True)
class PokemonSpecies:
    name: str

    types: tuple[str, ...]

    base_stats: Stats

    @classmethod
    def from_json(cls, json_data: dict, name: str):
        return PokemonSpecies(
            name=name,
            types=tuple(json_data["types"]),
            base_stats=Stats.from_json(json_data["base_stats"]),
        )
