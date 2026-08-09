from __future__ import annotations

from database.ability_database import AbilityDatabase
from database.item_database import ItemDatabase
from database.learnset_database import LearnsetDatabase
from database.move_database import MoveDatabase
from database.species_database import SpeciesDatabase
from pokemon_set import PokemonSet
from stats.evs import EVs
from stats.ivs import IVs
from stats.nature import Nature


class PokemonSetResolver:
    """Resolves configuration names into a validated PokemonSet."""

    def __init__(
        self,
        *,
        species_database: SpeciesDatabase,
        ability_database: AbilityDatabase,
        move_database: MoveDatabase,
        item_database: ItemDatabase,
        learnset_database: LearnsetDatabase,
    ) -> None:
        self._species_database = species_database
        self._ability_database = ability_database
        self._move_database = move_database
        self._item_database = item_database
        self._learnset_database = learnset_database

    def resolve(
        self,
        *,
        species_name: str,
        ability_name: str,
        move_names: tuple[str, ...],
        level: int,
        nature: Nature,
        ivs: IVs,
        evs: EVs,
        item_name: str | None = None,
    ) -> PokemonSet:
        species = self._species_database.get(species_name)
        ability = self._ability_database.get(ability_name)
        moves = tuple(self._move_database.get(name) for name in move_names)
        item = (
            self._item_database.get(item_name) if item_name is not None else None
        )
        learnset = self._learnset_database.get(species.name)

        return PokemonSet.from_components(
            species=species,
            level=level,
            nature=nature,
            ivs=ivs,
            evs=evs,
            moves=moves,
            ability=ability,
            learnset=learnset,
            item=item,
        )
