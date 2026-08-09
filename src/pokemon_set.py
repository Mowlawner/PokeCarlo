from dataclasses import dataclass

from ability import Ability
from item import Item
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

    item: Item | None = None

    @classmethod
    def from_components(
        cls,
        *,
        species: Species,
        level: int,
        nature: Nature,
        ivs: IVs,
        evs: EVs,
        moves: tuple[Move, ...],
        ability: Ability,
        learnset: frozenset[str],
        item: Item | None = None,
    ) -> "PokemonSet":
        cls._validate_learnset(species, moves, learnset)
        return cls(
            species=species,
            level=level,
            nature=nature,
            ivs=ivs,
            evs=evs,
            moves=moves,
            ability=ability,
            item=item,
        )

    def __post_init__(self) -> None:
        if not 1 <= len(self.moves) <= 4:
            raise ValueError("Pokemon must know between 1 and 4 moves.")
        if len(set(self.moves)) != len(self.moves):
            raise ValueError("Duplicate moves are not allowed.")

        ability_name = _normalize_name(self.ability.name)
        ability_names = self.species.abilities
        if ability_name not in ability_names:
            allowed = ", ".join(ability_names)
            raise ValueError(
                f"{ability_name} is not a valid ability for {self.species.name}. "
                f"Expected one of: {allowed}."
            )

    @staticmethod
    def _validate_learnset(
        species: Species,
        moves: tuple[Move, ...],
        learnset: frozenset[str],
    ) -> None:
        unavailable_moves = tuple(
            move.name for move in moves if move.name not in learnset
        )
        if unavailable_moves:
            available = ", ".join(sorted(learnset))
            unavailable = ", ".join(unavailable_moves)
            raise ValueError(
                f"{species.name} cannot learn: {unavailable}. "
                f"Expected one of: {available}."
            )


def _normalize_name(name: str) -> str:
    return name.upper().replace("-", "_").replace(" ", "_")
