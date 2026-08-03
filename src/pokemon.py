from dataclasses import dataclass

from move import Move
from pokemon_species import PokemonSpecies
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature
from stats.stat_calculator import calculate_stats
from stats.stat_stages import StatStages
from stats.stats import Stats


@dataclass(slots=True)
class Pokemon:
    species: PokemonSpecies

    level: int

    nature: Nature
    ivs: IVs
    evs: EVs

    stats: Stats
    current_hp: int

    stat_stages: StatStages

    moves: tuple[Move, ...]

    @classmethod
    def from_species(
        cls,
        species: PokemonSpecies,
        level: int,
        nature: Nature,
        ivs: IVs,
        evs: EVs,
        moves: tuple[Move, ...],
    ) -> "Pokemon":
        stats = calculate_stats(
            base_stats=species.base_stats,
            ivs=ivs,
            evs=evs,
            nature=nature,
            level=level,
        )

        return cls(
            species=species,
            level=level,
            nature=nature,
            ivs=ivs,
            evs=evs,
            stats=stats,
            current_hp=stats.hp,
            stat_stages=StatStages(),
            moves=moves,
        )
