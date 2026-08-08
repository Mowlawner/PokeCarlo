from dataclasses import dataclass

from pokemon_types import Type
from stats.base_stats import BaseStats


@dataclass(slots=True, frozen=True)
class Species:
    """Static data for one Pokémon species or form."""

    # ``name`` identifies the form (for example, LATIAS_MEGA), while
    # ``species_name`` identifies its base species (LATIAS).
    name: str
    display_name: str
    species_name: str
    pokemon_id: int
    national_dex: int
    types: tuple[Type, ...]
    base_stats: BaseStats
    abilities: tuple[str, ...]
