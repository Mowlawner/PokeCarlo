from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from pokemon_species import Species
from pokemon_types import Type
from stats.base_stats import BaseStats


class SpeciesDatabase:
    """A runtime database of generated Pokémon species and form data."""

    def __init__(self, species: dict[str, Species]):
        self._species = species

    @classmethod
    def load(cls, directory_path: str | Path) -> SpeciesDatabase:
        path = Path(directory_path)
        if not path.is_dir():
            raise ValueError(f"Path {directory_path} is not a directory.")

        species: dict[str, Species] = {}
        for json_file in path.glob("*.json"):
            try:
                with json_file.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                entry = cls._parse_species(data)
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid species data in {json_file}: {error}"
                ) from error

            if entry.name in species:
                raise ValueError(
                    f"Duplicate species name {entry.name!r} in {json_file}."
                )
            species[entry.name] = entry

        return cls(species)

    @staticmethod
    def _parse_species(data: Any) -> Species:
        if not isinstance(data, dict):
            raise TypeError("expected a JSON object")

        name = _parse_canonical_name(data["name"], "name")
        display_name = data["display_name"]
        if not isinstance(display_name, str) or not display_name.strip():
            raise ValueError("display_name must be a non-empty string")

        species_name = _parse_canonical_name(data["species_name"], "species_name")
        pokemon_id = _positive_int(data["pokemon_id"], "pokemon_id")
        national_dex = _positive_int(data["national_dex"], "national_dex")

        types = data["types"]
        abilities = data["abilities"]
        if not isinstance(types, list) or not types:
            raise ValueError("types must be a non-empty list")
        if len(types) > 2:
            raise ValueError("types must contain one or two types")
        if not isinstance(abilities, list):
            raise TypeError("abilities must be a list")

        parsed_types = tuple(Type[_normalize_name(value)] for value in types)
        if len(set(parsed_types)) != len(parsed_types):
            raise ValueError("types must not contain duplicates")

        return Species(
            name=name,
            display_name=display_name,
            species_name=species_name,
            pokemon_id=pokemon_id,
            national_dex=national_dex,
            types=parsed_types,
            base_stats=_parse_base_stats(data["base_stats"]),
            abilities=tuple(_canonical_string(value, "ability") for value in abilities),
        )

    def get(self, name: str) -> Species:
        return self._species[_normalize_name(name)]

    def __len__(self) -> int:
        return len(self._species)

    def __iter__(self) -> Iterator[Species]:
        return iter(self._species.values())


def _normalize_name(value: Any) -> str:
    return _canonical_string(value, "name").replace(" ", "_")


def _parse_canonical_name(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    if value != value.upper().replace("-", "_").replace(" ", "_"):
        raise ValueError(f"{field_name} must be a canonical identifier")
    return value


def _canonical_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.upper().replace("-", "_")


def _positive_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")
    return value


def _parse_base_stats(data: Any) -> BaseStats:
    if not isinstance(data, dict):
        raise TypeError("base_stats must be an object")

    values = {
        field_name: _positive_int(data[field_name], f"base_stats.{field_name}")
        for field_name in (
            "hp",
            "attack",
            "defense",
            "sp_attack",
            "sp_defense",
            "speed",
        )
    }
    return BaseStats(**values)
