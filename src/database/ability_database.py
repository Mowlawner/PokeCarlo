from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from ability import Ability


class AbilityDatabase:
    """A runtime database loaded from generated ability JSON files."""

    def __init__(self, abilities: dict[str, Ability]):
        self._abilities = abilities

    @classmethod
    def load(cls, directory_path: str | Path) -> AbilityDatabase:
        path = Path(directory_path)
        if not path.is_dir():
            raise ValueError(f"Path {directory_path} is not a directory.")

        abilities = {}
        for json_file in path.glob("*.json"):
            try:
                with json_file.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                ability = cls._parse_ability(data)
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid ability data in {json_file}: {error}"
                ) from error
            abilities[ability.name] = ability

        return cls(abilities)

    @staticmethod
    def _parse_ability(data: Any) -> Ability:
        if not isinstance(data, dict):
            raise TypeError("expected a JSON object")

        return Ability(
            name=data["ability_name"],
            display_name=data["display_name"],
            id=data["ability_id"],
            generation=data["generation"],
        )

    def get(self, name: str) -> Ability:
        return self._abilities[name.upper().replace("-", "_")]

    def __len__(self) -> int:
        return len(self._abilities)

    def __iter__(self) -> Iterator[Ability]:
        return iter(self._abilities.values())
